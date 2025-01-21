from fastapi import HTTPException, status
from typing import overload, Any
from bson import ObjectId

from app.schemas.user import AccountType, User
from app.schemas.tournament import Tournament
from app.schemas.bot import Bot, BotUpdate
from database.main import (
    Tournament as TournamentCollection,
    Bot as BotCollection,
    MongoDB,
)
import app.utils.connection as conn
import app.models.tournament as T
import app.models.game_type as G
import app.models.user as U


class DBBot:
    """
    Represents a bot model in the database.

    Attributes:
    ---
    id : ObjectId
        The unique identifier of the bot.
    name : str
        The name of the bot.
    game_type : ObjectId
        The game type the bot is associated with.
    code : bytes
        The code of the bot.
    is_validated : bool
        The validation status of the bot.
    games_played : int
        The number of games the bot has played.
    wins : int
        The number of games the bot has won.
    losses : int
        The number of games the bot has lost.
    total_tournaments : int
        The total number of tournaments the bot has participated in.
    tournaments_won : int
        The number of tournaments the bot has won.
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
        self._collection = BotCollection(db)

        if id is not None:
            self._from_id(id)
        elif data is not None:
            self._from_data(data)
        else:
            raise ValueError("DBBot must be initialized with either id or data.")

    def _from_data(self, data: dict[str, Any]) -> None:
        self.id: ObjectId = data["_id"]
        self.name: str = data["name"]
        self.game_type: ObjectId = data["game_type"]
        self.code: bytes = data["code"]
        self.is_validated: bool = data["is_validated"]
        self.games_played: int = data["games_played"]
        self.wins: int = data["wins"]
        self.losses: int = data["losses"]
        self.total_tournaments: int = data["total_tournaments"]
        self.tournaments_won: int = data["tournaments_won"]

    def _from_id(self, bot_id: ObjectId) -> None:
        data = self._collection.get_bot_by_id(bot_id)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bot: {bot_id} not found.",
            )

        self._from_data(data)

    def get_owner(self) -> User:
        """
        Retrieves the owner of the bot.
        """

        owner_data = self._collection.get_owner(self.id)
        if owner_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Owner of bot: {self.id} not found.",
            )

        db_owner = U.DBUser(self._db, id=owner_data["_id"])
        return db_owner.to_schema()

    def get_tournaments(self) -> list[Tournament]:
        """
        Retrieves all tournaments the bot has participated in.
        """

        collection = TournamentCollection(self._db)
        tournament_ids = collection.get_tournaments_by_bot_id(self.id)
        db_tournaments = [
            T.DBTournament(self._db, data=tournament) for tournament in tournament_ids
        ]

        return [db_tournament.to_schema() for db_tournament in db_tournaments]

    def check_access(self, user: User) -> bool:
        """
        Checks if the user has access to a specific bot.
        """

        is_admin: bool = user.account_type is AccountType.ADMIN
        is_owner: bool = self.get_owner().id == user.id

        return is_admin or is_owner

    def update(self, bot_data: BotUpdate) -> None:
        """
        Updates the bot in the database.
        """

        if bot_data.name is not None:
            self._collection.update_name(self.id, bot_data.name)

        self._from_id(self.id)

    def update_stats(self, winner: bool) -> None:
        """
        Updates the bot's stats in the database.
        """

        self._collection.update_stats(self.id, winner)
        self._from_id(self.id)

    def update_tournament_wins(self) -> None:
        """
        Updates the bot's tournament wins in the database.
        """

        # self._collection.update_tournament_wins(self.id)
        self._from_id(self.id)

    def delete(self) -> None:
        """
        Deletes the bot from the database.
        """

        self._collection.delete_bot(self.id)

    def to_schema(self, detail: bool = False) -> Bot:
        """
        Converts the model to a Bot schema.
        """

        db_game_type = G.DBGameType(self._db, id=self.game_type)
        game_type = db_game_type.to_schema()

        owner = self.get_owner()

        if detail:
            return Bot(
                _id=self.id,
                name=self.name,
                game_type=game_type,
                code=self.code,
                is_validated=self.is_validated,
                games_played=self.games_played,
                wins=self.wins,
                losses=self.losses,
                total_tournaments=self.total_tournaments,
                tournaments_won=self.tournaments_won,
                owner=owner,
            )
        return Bot(
            _id=self.id,
            name=self.name,
            game_type=game_type,
            is_validated=self.is_validated,
            games_played=self.games_played,
            wins=self.wins,
            losses=self.losses,
            total_tournaments=self.total_tournaments,
            tournaments_won=self.tournaments_won,
            owner=owner,
        )

    @classmethod
    def insert(
        cls,
        db: MongoDB,
        current_user: User,
        name: str,
        game_type_id: ObjectId,
        code: bytes,
    ) -> "DBBot":
        """
        Inserts a bot into the database.
        """

        db_game_type = G.DBGameType(db, id=game_type_id)
        game_type = db_game_type.to_schema()

        collection = BotCollection(db)
        bot_id = collection.create_bot(name, game_type.id, code)
        db_user = U.DBUser(db, id=current_user.id)
        db_user.add_bot(bot_id)

        if not conn.validate_bot(game_type.name, code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bot validation failed.",
            )

        collection.validate_bot(bot_id)
        return cls(db, id=bot_id)

    @staticmethod
    def get_all(db: MongoDB) -> list[Bot]:
        """
        Retrieves all bots from the database.
        """

        bots = db.get_all_bots()
        db_bots = [DBBot(db, data=bot) for bot in bots]
        return [db_bot.to_schema() for db_bot in db_bots]
