from app.schemas.bot import BotModel
from database.main import MongoDB, Bot
from bson import ObjectId
from typing import Any


def get_bot_by_id(bot_id: str) -> BotModel | None:
    db = MongoDB()
    bots = Bot(db)
    bot: dict[str, Any] | None = bots.get_bot_by_id(ObjectId(bot_id))

    if bot is None:
        return None

    return BotModel(
        id=str(bot["_id"]),
        name=str(bot["name"]),
        game_type=str(bot["game_type"]),
        code=str(bot["code"]),
        is_validated=bool(bot["is_validated"]),
        games_played=int(bot["games_played"]),
        wins=int(bot["wins"]),
        losses=int(bot["losses"]),
        total_tournaments=int(bot["total_tournaments"]),
        tournaments_won=int(bot["tournaments_won"]),
    )
