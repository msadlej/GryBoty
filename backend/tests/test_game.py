from app.models.game import insert_game_type
from app.schemas.game import GameTypeModel, GameTypeCreate


def test_game_model(game_dict):
    game = GameTypeModel(**game_dict)

    assert game.id == game_dict["_id"]
    assert game.name == game_dict["name"]
    assert game.description == game_dict["description"]


def test_insert_game_type(db_connection):
    game_create = GameTypeCreate(name="Chess", description="A strategic board game")
    game = insert_game_type(db_connection, game_create)

    assert isinstance(game, GameTypeModel)
    assert game.name == "Chess"
    assert game.description == "A strategic board game"
