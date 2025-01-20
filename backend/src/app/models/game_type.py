from fastapi import HTTPException, status
from typing import overload, Any
from bson import ObjectId

from database.main import MongoDB, GameType as GameTypeCollection
from app.schemas.game_type import GameType, GameTypeCreate


class DBGameType:
    """
    Represents a game type model in the database.

    Attributes:
    ---
    id : ObjectId
        The unique identifier of the game type.
    name : str
        The name of the game type.
    description : str
        The description of the game type.
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
        self._collection = GameTypeCollection(db)

        if id is not None:
            self._from_id(id)
        elif data is not None:
            self._from_data(data)
        else:
            raise ValueError("DBGameType must be initialized with either id or data.")

    def _from_data(self, data: dict[str, Any]) -> None:
        self.id: ObjectId = data["_id"]
        self.name: str = data["name"]
        self.description: str = data["description"]

    def _from_id(self, game_type_id: ObjectId) -> None:
        data = self._collection.get_game_type_by_id(game_type_id)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game type: {game_type_id} not found.",
            )

        self._from_data(data)

    def to_schema(self) -> GameType:
        """
        Converts the model to a GameType schema.
        """

        return GameType(_id=self.id, name=self.name, description=self.description)

    @classmethod
    def insert(cls, db: MongoDB, game: GameTypeCreate) -> "DBGameType":
        """
        Inserts a game type into the database.
        Returns the created game type.
        """

        collection = GameTypeCollection(db)
        game_id = collection.create_game_type(game.name, game.description)

        return cls(db, id=game_id)

    @staticmethod
    def get_all(db: MongoDB) -> list[GameType]:
        """
        Retrieves all game types from the database.
        """

        game_types = db.get_all_game_types()
        db_game_types = [DBGameType(db, data=game_type) for game_type in game_types]
        return [db_game_type.to_schema() for db_game_type in db_game_types]
