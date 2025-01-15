from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from app.schemas.user import AccountType, UserModel
from app.models.game import get_game_type_by_id
from app.schemas.bot import BotModel, BotUpdate
from database.main import MongoDB, User, Bot
import app.utils.connection as conn


def check_bot_access(db: MongoDB, current_user: UserModel, bot_id: ObjectId) -> bool:
    """
    Checks if the current user has access to a specific bot.
    """

    if current_user.bots is None:
        current_user.bots = get_bots_by_user_id(db, current_user.id)

    is_admin: bool = current_user.account_type is AccountType.ADMIN
    return any(bot.id == bot_id for bot in current_user.bots) or is_admin


def get_bot_by_id(db: MongoDB, bot_id: ObjectId) -> dict[str, Any]:
    """
    Retrieves a bot from the database by its ID.
    Raises an error if the bot does not exist.
    """

    bots_collection = Bot(db)
    bot = bots_collection.get_bot_by_id(bot_id)

    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot: {bot_id} not found.",
        )

    return bot


def convert_bot(db: MongoDB, bot_dict: dict[str, Any]) -> BotModel:
    """
    Converts a dictionary to a BotModel object.
    """

    game_type = bot_dict.pop("game_type")
    bot_dict["game_type"] = get_game_type_by_id(db, game_type)

    return BotModel(**bot_dict)


def get_bots_by_user_id(db: MongoDB, user_id: ObjectId) -> list[BotModel]:
    """
    Retrieves all bots from the database that belong to a specific user.
    """

    users_collection = User(db)
    user = users_collection.get_user_by_id(user_id)

    if user is None:
        return []

    return [
        convert_bot(db, bot_dict)
        for bot_id in user["bots"]
        if (bot_dict := get_bot_by_id(db, bot_id))
    ]


def get_all_bots(db: MongoDB) -> list[BotModel]:
    """
    Retrieves all bots from the database.
    """

    bots = db.get_all_bots()

    return [convert_bot(db, bot) for bot in bots]


def insert_bot(
    db: MongoDB,
    current_user: UserModel,
    name: str,
    game_id: ObjectId,
    code: bytes,
) -> BotModel:
    """
    Inserts a bot into the database.
    Returns the created bot.
    """

    game = get_game_type_by_id(db, game_id)

    bots_collection = Bot(db)
    bot_id = bots_collection.create_bot(name, game.id, code)

    users_collection = User(db)
    users_collection.add_bot(current_user.id, bot_id)

    if not conn.validate_bot(game.name, code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bot validation failed.",
        )

    bots_collection.validate_bot(bot_id)

    bot_dict = get_bot_by_id(db, bot_id)
    return convert_bot(db, bot_dict)


def update_bot(db, bot_id: ObjectId, bot_data: BotUpdate) -> BotModel:
    """
    Updates the name of a bot in the database.
    Returns the updated bot.
    """

    bots_collection = Bot(db)

    if bot_data.name is not None:
        bots_collection.update_name(bot_id, bot_data.name)

    bot_dict = get_bot_by_id(db, bot_id)
    return convert_bot(db, bot_dict)
