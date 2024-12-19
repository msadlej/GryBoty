from app.schemas.game import GameModel
from database.main import MongoDB, GameType
from typing import Any


def get_all_game_types() -> list[GameModel]:
    """
    Retrieves all game types from the database.
    """

    db = MongoDB()
    game_types: list[dict[str, Any]] = db.get_all_game_types()

    return [GameModel(**game) for game in game_types]
