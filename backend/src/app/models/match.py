from fastapi import HTTPException, status
from typing import overload, Any
from bson import ObjectId

from database.main import MongoDB, Match as MatchCollection
from app.schemas.match import Match, MatchCreate
from app.models.tournament import DBTournament
import app.utils.connection as conn
from app.models.bot import DBBot
from app.schemas.bot import Bot


class DBMatch:
    @overload
    def __init__(self, db: MongoDB, /, *, id: ObjectId) -> None: ...

    @overload
    def __init__(self, db: MongoDB, /, *, data: dict[str, Any]) -> None: ...

    def __init__(
        self,
        db: MongoDB,
        /,
        *,
        id: ObjectId | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        self._db = db
        self._collection = MatchCollection(db)

        if id is not None:
            self._from_id(id)
        elif data is not None:
            self._from_data(data)
        else:
            raise ValueError("DBMatch must be initialized with either id or data.")

    def _from_data(self, data: dict[str, Any]) -> None:
        self.id: ObjectId = data["_id"]
        self.game_num: int = data["game_num"]
        self.players: tuple[ObjectId, ObjectId] = data["players"].values()
        self.moves: list[str] = data["moves"]
        self.winner: ObjectId | None = data["winner"]

    def _from_id(self, match_id: ObjectId) -> None:
        data = self._collection.get_match_by_id(match_id)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Match: {match_id} not found.",
            )

        self._from_data(data)

    def get_players(self, detail: bool = False) -> tuple[Bot, Bot]:
        """
        Retrieves the players of the match.
        """

        id_0, id_1 = self.players
        db_players = DBBot(self._db, id=id_0), DBBot(self._db, id=id_1)
        bot_0 = db_players[0].to_schema(detail=detail)
        bot_1 = db_players[1].to_schema(detail=detail)

        return bot_0, bot_1

    def run(self) -> dict[str, Bot]:
        """
        Runs the match on docker.
        Updates the database with the results of a match.
        Returns the winner and loser bots with updated stats.
        """

        bot_0, bot_1 = self.get_players(detail=True)
        game_type = bot_0.game_type
        assert bot_0.game_type == bot_1.game_type
        assert bot_0.code is not None
        assert bot_1.code is not None

        response = conn.run_match(game_type.name, bot_0.code, bot_1.code)
        i = 0

        while response["winner"] is None:
            response = conn.run_match(game_type.name, bot_0.code, bot_1.code)
            i += 1

            if i > 9:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Match: {self.id} ended in a draw.",
                )

        moves: list[str] = response["states"]
        if response["winner"] == 0:
            winner = bot_0
            loser = bot_1
        else:
            winner = bot_1
            loser = bot_0

        self._collection.set_winner(self.id, winner.id)
        for move in moves:
            self._collection.add_move(self.id, move)

        db_winner = DBBot(self._db, id=winner.id)
        db_loser = DBBot(self._db, id=loser.id)
        db_winner.update_stats(True)
        db_loser.update_stats(False)

        return {
            "winner": db_winner.to_schema(),
            "loser": db_loser.to_schema(),
        }

    def to_schema(self, detail: bool = False) -> Match:
        """
        Converts the model to a Match schema.
        """

        players = self.get_players()

        db_winner = DBBot(self._db, id=self.winner) if self.winner else None
        winner = db_winner.to_schema() if db_winner else None

        result = Match(
            _id=self.id,
            game_num=self.game_num,
            players=players,
            winner=winner,
        )

        if detail:
            result.moves = self.moves
        return result

    @classmethod
    def insert(
        cls,
        db: MongoDB,
        tournament_id: ObjectId,
        match_data: MatchCreate,
    ) -> "DBMatch":
        """
        Creates a new match in the database.
        Returns the created match.
        """

        collection = MatchCollection(db)
        match_id = collection.create_match(
            match_data.game_num, match_data.players[0], match_data.players[1]
        )

        db_tournament = DBTournament(db, id=tournament_id)
        db_tournament.add_match(match_id)

        return cls(db, id=match_id)

    @staticmethod
    def get_by_tournament_id(db: MongoDB, tournament_id: ObjectId) -> list[Match]:
        """
        Retrieves all matches from the database that belong to a specific tournament.
        """

        db_tournament = DBTournament(db, id=tournament_id)
        db_matches = [DBMatch(db, id=match_id) for match_id in db_tournament.matches]

        return [db_match.to_schema() for db_match in db_matches]
