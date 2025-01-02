from app.utils.database import get_db_connection
from fastapi import HTTPException, status
from app.schemas.game import GameModel
from database.main import GameType
from bson import ObjectId


def get_game_type_by_id(game_id: ObjectId) -> GameModel:
    """
    Retrieves a game type from the database by its ID.
    Raises an error if the game type does not exist.
    """

    with get_db_connection() as db:
        game_collection = GameType(db)
        game = game_collection.get_game_type_by_id(game_id)

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

    with get_db_connection() as db:
        game_types = db.get_all_game_types()

    return [GameModel(**game) for game in game_types]
