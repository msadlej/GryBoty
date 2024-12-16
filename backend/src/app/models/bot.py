from database.main import MongoDB, Bot
from app.schemas.bot import BotModel
from bson import ObjectId
from typing import Any


def get_bot_by_id(bot_id: str) -> BotModel | None:
    db = MongoDB()
    bots = Bot(db)
    bot: dict[str, Any] | None = bots.get_bot_by_id(ObjectId(bot_id))

    if bot is None:
        return None

    return BotModel(**bot)


def get_all_bots() -> list[BotModel]:
    db = MongoDB()
    all_bots: list[dict[str, Any]] = db.get_all_bots()

    return [BotModel(**bot) for bot in all_bots]
