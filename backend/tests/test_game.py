from app.models.game import insert_game_type
from app.schemas.game import GameModel, GameCreate


def test_game_model(game_dict):
    game = GameModel(**game_dict)

    assert game.id == game_dict["_id"]
    assert game.name == game_dict["name"]
    assert game.description == game_dict["description"]


def test_insert_game_type(db_connection):
    game_create = GameCreate(name="Chess", description="A strategic board game")
    game = insert_game_type(db_connection, game_create)

    assert isinstance(game, GameModel)
    assert game.name == "Chess"
    assert game.description == "A strategic board game"
