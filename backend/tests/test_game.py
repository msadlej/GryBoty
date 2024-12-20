from app.schemas.game import GameModel
from bson import ObjectId


def test_game_model(game_dict):
    game = GameModel(**game_dict)

    assert ObjectId(game.id) == game_dict["_id"]
    assert game.name == game_dict["name"]
    assert game.description == game_dict["description"]
