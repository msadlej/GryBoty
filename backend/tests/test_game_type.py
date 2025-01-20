from fastapi import HTTPException
import pytest

from app.schemas.game_type import GameType, GameTypeCreate
from app.models.game_type import DBGameType


def test_game_schema(game_type_dict):
    game_type = GameType(**game_type_dict)

    assert game_type.id == game_type_dict["_id"]
    assert game_type.name == game_type_dict["name"]
    assert game_type.description == game_type_dict["description"]


class TestGameModel:
    def test_init_data(self, db_connection, game_type_dict):
        db_game_type = DBGameType(db_connection, data=game_type_dict)

        assert db_game_type.id == game_type_dict["_id"]
        assert db_game_type.name == game_type_dict["name"]
        assert db_game_type.description == game_type_dict["description"]

    def test_init_id(self, db_connection, game_type_dict):
        with pytest.raises(HTTPException):
            _ = DBGameType(db_connection, id=game_type_dict["_id"])

    def test_to_schema(self, db_connection, game_type_dict):
        db_game_type = DBGameType(db_connection, data=game_type_dict)
        game_type = GameType(**game_type_dict)

        assert db_game_type.to_schema() == game_type

    def test_insert(self, db_connection, game_type_dict):
        game_type = GameTypeCreate(**game_type_dict)
        db_game_type = DBGameType.insert(db_connection, game_type)

        assert db_game_type.name == game_type_dict["name"]
        assert db_game_type.description == game_type_dict["description"]

    def test_get_all(self, db_connection, game_type_dict):
        game_type = GameTypeCreate(**game_type_dict)
        db_game_type = DBGameType.insert(db_connection, game_type)
        game_types = DBGameType.get_all(db_connection)

        assert len(game_types) == 1
        assert game_types[0].name == db_game_type.name
        assert game_types[0].description == db_game_type.description
