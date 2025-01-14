from app.models.bot import convert_bot, insert_bot
from app.models.game import insert_game_type
from app.schemas.game import GameCreate
from app.schemas.user import UserModel
from app.schemas.bot import BotModel


def test_bot_model(bot_dict):
    bot = BotModel(**bot_dict)

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


def test_convert_bot(bot_dict):
    bot = convert_bot(..., bot_dict, detail=False)

    assert bot.game_type is None


def test_insert_bot(db_connection, user_dict, monkeypatch):
    game_create = GameCreate(name="Chess", description="A strategic board game")
    game = insert_game_type(db_connection, game_create)
    user = UserModel(**user_dict)

    monkeypatch.setattr("app.models.bot.conn.validate_bot", lambda *args: True)
    bot = insert_bot(db_connection, user, "Bot", game.id, b"print('Hello, World!')")

    assert isinstance(bot, BotModel)
    assert bot.name == "Bot"
    assert bot.game_type == game
    assert bot.is_validated is True
    assert bot.games_played == 0
    assert bot.wins == 0
    assert bot.losses == 0
    assert bot.total_tournaments == 0
    assert bot.tournaments_won == 0
