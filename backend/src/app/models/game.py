from fastapi import HTTPException, status
from bson import ObjectId

from app.schemas.game import GameTypeModel, GameTypeCreate
from database.main import MongoDB, GameType


def get_game_type_by_id(db: MongoDB, game_id: ObjectId) -> GameTypeModel:
    """
    Retrieves a game type from the database by its ID.
    Raises an error if the game type does not exist.
    """

    game_collection = GameType(db)
    game = game_collection.get_game_type_by_id(game_id)

    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game: {game_id} not found.",
        )

    return GameTypeModel(**game)


def get_all_game_types(db: MongoDB) -> list[GameTypeModel]:
    """
    Retrieves all game types from the database.
    """

    game_types = db.get_all_game_types()

    return [GameTypeModel(**game) for game in game_types]


def insert_game_type(db: MongoDB, game: GameTypeCreate) -> GameTypeModel:
    """
    Inserts a game type into the database.
    Returns the created game type.
    """

    game_collection = GameType(db)
    game_id = game_collection.create_game_type(game.name, game.description)

    return get_game_type_by_id(db, game_id)
