from app.schemas.user import UserModel, AccountType
from database.main import MongoDB, Bot
from app.schemas.bot import BotModel
from bson import ObjectId
from typing import Any


def check_bot_access(current_user: UserModel, bot_id: str) -> bool:
    """
    Checks if the current user has access to a specific bot.
    """

    return bot_id in current_user.bots or current_user.account_type == AccountType.ADMIN


def get_bot_by_id(bot_id: str) -> BotModel | None:
    """
    Retrieves a bot from the database by its ID.
    Returns None if the bot does not exist.
    """

    db = MongoDB()
    bots = Bot(db)
    bot: dict[str, Any] | None = bots.get_bot_by_id(ObjectId(bot_id))

    return BotModel(**bot) if bot is not None else None


def get_own_bots(current_user: UserModel) -> list[BotModel]:
    """
    Retrieves all bots from the database that belong to the current user.
    """

    return [
        bot
        for bot_id in current_user.bots
        if (bot := get_bot_by_id(bot_id)) is not None
    ]


def get_all_bots() -> list[BotModel]:
    """
    Retrieves all bots from the database.
    """

    db = MongoDB()
    all_bots: list[dict[str, Any]] = db.get_all_bots()

    return [BotModel(**bot) for bot in all_bots]
