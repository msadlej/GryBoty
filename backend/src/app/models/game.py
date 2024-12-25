from database.main import MongoDB, GameType
from fastapi import HTTPException, status
from app.schemas.game import GameModel
from bson import ObjectId
from typing import Any


def get_game_type_by_id(game_id: str) -> GameModel:
    """
    Retrieves a game type from the database by its ID.
    Raises an error if the game type does not exist.
    """

    db = MongoDB()
    game_collection = GameType(db)
    game: dict[str, Any] | None = game_collection.get_game_type_by_id(ObjectId(game_id))

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game: {game_id} not found.",
        )

    return GameModel(**game)


def get_all_game_types() -> list[GameModel]:
    """
    Retrieves all game types from the database.
    """

    db = MongoDB()
    game_types: list[dict[str, Any]] = db.get_all_game_types()

    return [GameModel(**game) for game in game_types]
