from app.schemas.user import AccountType, UserModel
from app.models.game import get_game_type_by_id
from database.main import MongoDB, User, Bot
from app.schemas.game import GameModel
from app.schemas.bot import BotModel
from bson import ObjectId
from typing import Any


def check_bot_access(current_user: UserModel, bot_id: str) -> bool:
    """
    Checks if the current user has access to a specific bot.
    """

    if current_user.bots is None:
        current_user.bots = get_own_bots(current_user)

    is_admin: bool = current_user.account_type == AccountType.ADMIN
    return any(bot.id == bot_id for bot in current_user.bots) or is_admin


def get_bot_by_id(bot_id: str) -> dict[str, Any] | None:
    """
    Retrieves a bot from the database by its ID.
    Returns None if the bot does not exist.
    """

    db = MongoDB()
    bots_collection = Bot(db)
    return bots_collection.get_bot_by_id(ObjectId(bot_id))


def convert_bot(bot_dict: dict[str, Any]) -> BotModel:
    """
    Converts a dictionary to a BotModel object.
    """

    game_type: GameModel | None = get_game_type_by_id(bot_dict["game_type"])
    bot_dict.pop("game_type")

    return BotModel(**bot_dict, game_type=game_type)


def get_own_bots(current_user: UserModel) -> list[BotModel]:
    """
    Retrieves all bots from the database that belong to the current user.
    """

    db = MongoDB()
    users_collection = User(db)
    user: dict[str, Any] | None = users_collection.get_user_by_id(
        ObjectId(current_user.id)
    )
    if user is None:
        return []

    bots: list[dict[str, Any]] = [
        bot for bot_id in user["bots"] if (bot := get_bot_by_id(bot_id)) is not None
    ]

    result: list[BotModel] = []
    for bot in bots:
        bot.pop("game_type")
        result.append(BotModel(**bot))

    return result


def get_all_bots() -> list[BotModel]:
    """
    Retrieves all bots from the database.
    """

    db = MongoDB()
    bots: list[dict[str, Any]] = db.get_all_bots()

    result: list[BotModel] = []
    for bot in bots:
        bot.pop("game_type")
        result.append(BotModel(**bot))

    return result
