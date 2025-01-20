from fastapi import HTTPException
import pytest

from app.models.bot import DBBot
from app.schemas.bot import Bot


def test_bot_schema(bot_dict):
    bot = Bot(**bot_dict)

    assert bot.id == bot_dict["_id"]
    assert bot.name == bot_dict["name"]
    assert bot.game_type == bot_dict["game_type"]
    assert bot.code == bot_dict["code"]
    assert bot.is_validated == bot_dict["is_validated"]
    assert bot.games_played == bot_dict["games_played"]
    assert bot.wins == bot_dict["wins"]
    assert bot.losses == bot_dict["losses"]
    assert bot.total_tournaments == bot_dict["total_tournaments"]
    assert bot.tournaments_won == bot_dict["tournaments_won"]
    assert bot.owner == bot_dict["owner"]


class TestBotModel:
    def test_init_data(self, db_connection, bot_dict):
        db_bot = DBBot(db_connection, data=bot_dict)

        assert db_bot.id == bot_dict["_id"]
        assert db_bot.name == bot_dict["name"]
        assert db_bot.game_type == bot_dict["game_type"]
        assert db_bot.code == bot_dict["code"]
        assert db_bot.is_validated == bot_dict["is_validated"]
        assert db_bot.games_played == bot_dict["games_played"]
        assert db_bot.wins == bot_dict["wins"]
        assert db_bot.losses == bot_dict["losses"]
        assert db_bot.total_tournaments == bot_dict["total_tournaments"]
        assert db_bot.tournaments_won == bot_dict["tournaments_won"]

    def test_init_id(self, db_connection, bot_dict):
        with pytest.raises(HTTPException):
            _ = DBBot(db_connection, id=bot_dict["_id"])

    def test_to_schema(self, bot_dict, insert_bot):
        db_game_type, db_user, db_bot = insert_bot
        bot_dict["game_type"] = db_game_type.to_schema()
        bot_dict["owner"] = db_user.to_schema()
        bot_dict["_id"] = db_bot.id
        bot = Bot(**bot_dict)

        assert db_bot.to_schema(detail=True) == bot
        assert db_bot.to_schema().code is None

    def test_insert(self, bot_dict, insert_bot):
        db_game_type, _, db_bot = insert_bot

        assert db_bot.name == bot_dict["name"]
        assert db_bot.game_type == db_game_type.id
        assert db_bot.code == bot_dict["code"]
        assert db_bot.is_validated
        assert db_bot.games_played == 0
        assert db_bot.wins == 0
        assert db_bot.losses == 0
        assert db_bot.total_tournaments == 0
        assert db_bot.tournaments_won == 0

    def test_get_all(self, db_connection, insert_bot):
        _, _, db_bot = insert_bot
        bots = DBBot.get_all(db_connection)

        assert len(bots) == 1
        assert bots[0].name == db_bot.name
        assert bots[0].game_type.id == db_bot.game_type
        assert bots[0].code is None
        assert bots[0].is_validated == db_bot.is_validated
        assert bots[0].games_played == db_bot.games_played
        assert bots[0].wins == db_bot.wins
        assert bots[0].losses == db_bot.losses
        assert bots[0].total_tournaments == db_bot.total_tournaments
        assert bots[0].tournaments_won == db_bot.tournaments_won
