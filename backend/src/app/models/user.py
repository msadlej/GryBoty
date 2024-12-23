from app.models.bot import get_bot_by_id, convert_bot
from database.main import MongoDB, User
from app.schemas.user import UserModel
from bson import ObjectId
from typing import Any


def get_user_by_id(user_id: str | None = None) -> dict[str, Any] | None:
    """
    Retrieves a user from the database by their ID.
    Returns None if the user does not exist.
    """

    if user_id is None:
        return None

    db = MongoDB()
    users_collection = User(db)
    return users_collection.get_user_by_id(ObjectId(user_id))


def get_user_by_username(username: str | None = None) -> dict[str, Any] | None:
    """
    Retrieves a user from the database by their username.
    Returns None if the user does not exist.
    """

    if username is None:
        return None

    db = MongoDB()
    users_collection = User(db)
    return users_collection.get_user_by_username(username)


def convert_user(user_dict: dict[str, Any], detail: bool = False) -> UserModel:
    """
    Converts a dictionary to a UserModel object.
    """

    bots: list[str] = user_dict.pop("bots")
    if not detail:
        return UserModel(**user_dict)

    user_dict["bots"] = [
        convert_bot(bot)
        for bot_id in bots
        if (bot := get_bot_by_id(bot_id)) is not None
    ]

    return UserModel(**user_dict)


def get_all_users() -> list[UserModel]:
    """
    Retrieves all users from the database
    """

    db = MongoDB()
    users: list[dict[str, Any]] = db.get_all_users()

    return [convert_user(user) for user in users]


def insert_user(username, password) -> dict[str, Any] | None:
    """
    Inserts a new user into the database.
    Returns the new user if successful.
    Returns None if the user already exists.
    """

    db = MongoDB()
    users_collection = User(db)
    if get_user_by_username(username) is None:
        return None

    user_id: ObjectId = users_collection.create_user(username, password, "standard")
    new_user: dict[str, Any] | None = get_user_by_id(str(user_id))

    return new_user
