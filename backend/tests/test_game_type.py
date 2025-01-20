from app.schemas.game_type import GameType


def test_game_schema(game_type_dict):
    game_type = GameType(**game_type_dict)

    assert game_type.id == game_type_dict["_id"]
    assert game_type.name == game_type_dict["name"]
    assert game_type.description == game_type_dict["description"]
