from fastapi import HTTPException
import pytest

from app.models.match import DBMatch
from app.schemas.match import Match
from app.models.bot import DBBot


def test_match_schema(match_dict):
    match = Match(**match_dict)

    assert match.id == match_dict["_id"]
    assert match.game_num == match_dict["game_num"]
    assert match.players == match_dict["players"]
    assert match.moves == match_dict["moves"]
    assert match.winner == match_dict["winner"]


class TestMatchModel:
    def test_init_data(self, db_connection, match_dict):
        db_match = DBMatch(db_connection, data=match_dict)

        assert db_match.id == match_dict["_id"]
        assert db_match.game_num == match_dict["game_num"]
        assert db_match.players == match_dict["players"]
        assert db_match.moves == match_dict["moves"]
        assert db_match.winner == match_dict["winner"]

    def test_init_id(self, db_connection, match_dict):
        with pytest.raises(HTTPException):
            _ = DBMatch(db_connection, id=match_dict["_id"])

    def test_to_schema(self, db_connection, match_dict, insert_match):
        db_match = insert_match[5]
        match_dict["players"] = [
            db_bot.to_schema()
            for bot_id in db_match.players
            if (db_bot := DBBot(db_connection, id=bot_id))
        ]
        match_dict["_id"] = db_match.id
        match = Match(**match_dict)

        assert db_match.to_schema(detail=True) == match
        assert db_match.to_schema().moves is None

    def test_insert(self, match_dict, insert_match):
        db_match = insert_match[5]

        assert db_match.game_num == match_dict["game_num"]
        assert len(db_match.players) == 2
        assert db_match.moves == []
        assert db_match.winner is None
