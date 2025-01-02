from app.schemas.user import AccountType, UserModel
from app.utils.database import get_db_connection
from app.models.game import get_game_type_by_id
from fastapi import HTTPException, status
from app.schemas.bot import BotModel
from database.main import User, Bot
from bson import ObjectId
from typing import Any


def check_bot_access(current_user: UserModel, bot_id: ObjectId) -> bool:
    """
    Checks if the current user has access to a specific bot.
    """

    if current_user.bots is None:
        current_user.bots = get_own_bots(current_user)

    is_admin: bool = current_user.account_type is AccountType.ADMIN
    return any(bot.id == bot_id for bot in current_user.bots) or is_admin


def get_bot_by_id(bot_id: ObjectId) -> dict[str, Any]:
    """
    Retrieves a bot from the database by its ID.
    Raises an error if the bot does not exist.
    """

    with get_db_connection() as db:
        bots_collection = Bot(db)
        bot = bots_collection.get_bot_by_id(bot_id)

    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot: {bot_id} not found.",
        )

    return bot


def convert_bot(bot_dict: dict[str, Any], detail: bool = False) -> BotModel:
    """
    Converts a dictionary to a BotModel object.
    """

    game_type = bot_dict.pop("game_type")
    if not detail:
        return BotModel(**bot_dict)

    bot_dict["game_type"] = get_game_type_by_id(game_type)

    return BotModel(**bot_dict)


def get_bots_by_user_id(user_id: ObjectId) -> list[BotModel]:
    """
    Retrieves all bots from the database that belong to a specific user.
    """

    with get_db_connection() as db:
        users_collection = User(db)
        user = users_collection.get_user_by_id(user_id)

    if user is None:
        return []

    return [
        convert_bot(bot_dict)
        for bot_id in user["bots"]
        if (bot_dict := get_bot_by_id(bot_id))
    ]


def get_own_bots(current_user: UserModel) -> list[BotModel]:
    """
    Retrieves all bots from the database that belong to the current user.
    """

    return get_bots_by_user_id(current_user.id)


def get_all_bots() -> list[BotModel]:
    """
    Retrieves all bots from the database.
    """

    with get_db_connection() as db:
        bots = db.get_all_bots()

    return [convert_bot(bot) for bot in bots]


def insert_bot(current_user: UserModel, name: str, game_type: ObjectId) -> BotModel:
    """
    Inserts a bot into the database.
    """

    with get_db_connection() as db:
        bots_collection = Bot(db)
        bot_id = bots_collection.create_bot(name, game_type, f"{current_user.id}/")

        # code = f"{current_user.id}/{bot_id}"  TODO: Implement in db

        users_collection = User(db)
        users_collection.add_bot(current_user.id, bot_id)

    # TODO: Save the file in docker

    bot_dict = get_bot_by_id(bot_id)
    return convert_bot(bot_dict, detail=True)


def update_bot_name(bot_id: ObjectId, name: str) -> BotModel:
    """
    Updates the name of a bot in the database.
    """

    # with get_db_connection() as db:
    #     bots_collection = Bot(db)
    #     bots_collection.update_bot_name(bot_id, name)  TODO: Implement in db

    bot_dict = get_bot_by_id(bot_id)
    return convert_bot(bot_dict)
