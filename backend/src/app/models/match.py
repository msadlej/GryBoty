from fastapi import HTTPException, status
from typing import overload, Any
from bson import ObjectId

from database.main import MongoDB, Match as MatchCollection
from app.schemas.match import Match, MatchCreate
from app.schemas.bot import Bot
import app.utils.connection as conn
import app.models.tournament as T
import app.models.bot as B


class DBMatch:
    """
    Represents a match model in the database.

    Attributes:
    ---
    id : ObjectId
        The unique identifier of the match.
    game_num : int
        The number of the game in the tournament.
    players : tuple[ObjectId, ObjectId]
        The unique identifiers of the players.
    moves : list[str]
        The moves of the match.
    winner : ObjectId
        The unique identifier of the winner of the match.
    """

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
        self.players: tuple[ObjectId, ObjectId] = data["players"]
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
        db_players = B.DBBot(self._db, id=id_0), B.DBBot(self._db, id=id_1)
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

        db_winner = B.DBBot(self._db, id=winner.id)
        db_loser = B.DBBot(self._db, id=loser.id)
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

        db_winner = B.DBBot(self._db, id=self.winner) if self.winner else None
        winner = db_winner.to_schema() if db_winner else None

        if detail:
            return Match(
                _id=self.id,
                game_num=self.game_num,
                players=players,
                moves=self.moves,
                winner=winner,
            )
        return Match(
            _id=self.id,
            game_num=self.game_num,
            players=players,
            moves=None,
            winner=winner,
        )

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

        db_tournament = T.DBTournament(db, id=tournament_id)
        for player_id in match_data.player_0_id, match_data.player_1_id:
            if player_id not in db_tournament.participants:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Bot: {player_id} is not a participant in the tournament.",
                )

        collection = MatchCollection(db)
        match_id = collection.create_match(
            match_data.game_num, match_data.player_0_id, match_data.player_1_id
        )
        db_tournament.add_match(match_id)

        return cls(db, id=match_id)
