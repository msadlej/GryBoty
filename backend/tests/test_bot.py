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
