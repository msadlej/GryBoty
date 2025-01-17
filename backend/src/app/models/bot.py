from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from app.schemas.user import AccountType, UserModel
from app.models.game import get_game_type_by_id
from app.schemas.bot import BotModel, BotUpdate
from database.main import MongoDB, User, Bot
import app.utils.connection as conn


def get_bot_by_id(db: MongoDB, bot_id: ObjectId) -> BotModel:
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

    return convert_bot(db, bot)


def check_bot_access(db: MongoDB, current_user: UserModel, bot_id: ObjectId) -> bool:
    """
    Checks if the current user has access to a specific bot.
    """

    bot = get_bot_by_id(db, bot_id)

    is_admin: bool = current_user.account_type is AccountType.ADMIN
    is_creator: bool = bot.creator == current_user

    return is_admin or is_creator


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

    return [get_bot_by_id(db, bot_id) for bot_id in user["bots"]]


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

    return get_bot_by_id(db, bot_id)


def update_bot(db, bot_id: ObjectId, bot_data: BotUpdate) -> BotModel:
    """
    Updates the name of a bot in the database.
    Returns the updated bot.
    """

    bots_collection = Bot(db)

    if bot_data.name is not None:
        bots_collection.update_name(bot_id, bot_data.name)

    return get_bot_by_id(db, bot_id)


def delete_bot(db: MongoDB, bot_id: ObjectId) -> None:
    """
    Deletes a bot from the database.
    """

    bots_collection = Bot(db)
    bots_collection.delete_bot(bot_id)
