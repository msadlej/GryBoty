from app.schemas.game import GameModel


def test_game_model(game_dict):
    game = GameModel(**game_dict)

    assert game.id == game_dict["_id"]
    assert game.name == game_dict["name"]
    assert game.description == game_dict["description"]
