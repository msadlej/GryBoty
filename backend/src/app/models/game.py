from database.main import MongoDB, GameType
from app.schemas.game import GameModel
from bson import ObjectId
from typing import Any


def get_game_type_by_id(game_id: str) -> GameModel | None:
    """
    Retrieves a game type from the database by its ID.
    Returns None if the game type does not exist.
    """

    db = MongoDB()
    game_collection = GameType(db)
    game: dict[str, Any] | None = game_collection.get_game_type_by_id(ObjectId(game_id))

    return GameModel(**game) if game is not None else None


def get_all_game_types() -> list[GameModel]:
    """
    Retrieves all game types from the database.
    """

    db = MongoDB()
    game_types: list[dict[str, Any]] = db.get_all_game_types()

    return [GameModel(**game) for game in game_types]
