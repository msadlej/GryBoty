from app.schemas.user import AccountType, UserModel, UserUpdate
from app.models.bot import get_bot_by_id, convert_bot
from app.utils.database import get_db_connection
from fastapi import HTTPException, status
from database.main import User
from bson import ObjectId
from typing import Any


def get_user_by_id(user_id: ObjectId) -> dict[str, Any]:
    """
    Retrieves a user from the database by their ID.
    Raises an error if the user does not exist.
    """

    with get_db_connection() as db:
        users_collection = User(db)
        user = users_collection.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User: {user_id} not found."
        )

    return user


def get_user_by_username(username: str | None = None) -> dict[str, Any] | None:
    """
    Retrieves a user from the database by their username.
    Returns None if the user does not exist.
    """

    if username is None:
        return None

    with get_db_connection() as db:
        users_collection = User(db)
        user = users_collection.get_user_by_username(username)

    return user


def convert_user(user_dict: dict[str, Any], detail: bool = False) -> UserModel:
    """
    Converts a dictionary to a UserModel object.
    """

    bots = user_dict.pop("bots")
    if not detail:
        return UserModel(**user_dict)

    user_dict["bots"] = [
        convert_bot(bot_dict) for bot_id in bots if (bot_dict := get_bot_by_id(bot_id))
    ]

    return UserModel(**user_dict)


def get_all_users() -> list[UserModel]:
    """
    Retrieves all users from the database
    """

    with get_db_connection() as db:
        users = db.get_all_users()

    return [convert_user(user) for user in users]


def insert_user(username, password) -> dict[str, Any]:
    """
    Inserts a new user into the database.
    Returns the new user if successful.
    Raises an error if the user already exists.
    """

    if get_user_by_username(username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User: {username} already exists",
        )

    with get_db_connection() as db:
        users_collection = User(db)
        user_id = users_collection.create_user(username, password, "standard")

    new_user = get_user_by_id(user_id)
    return new_user


def update_user_password(user_id: ObjectId, hashed_password: str) -> dict[str, Any]:
    """
    Updates a user's password in the database.
    """

    with get_db_connection() as db:
        users_collection = User(db)
        users_collection.update_password(user_id, hashed_password)

    return get_user_by_id(user_id)


def update_user(user_id: ObjectId, user_data: UserUpdate) -> UserModel:
    """
    Updates a user.
    Returns the updated user.
    Raises an error if the given account type is invalid.
    """

    if user_data.account_type is AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update user to admin.",
        )

    with get_db_connection() as db:
        users_collection = User(db)

        if user_data.account_type is not None:
            users_collection.update_account_type(user_id, user_data.account_type)

        if user_data.is_banned is not None:
            users_collection.update_ban(user_id, user_data.is_banned)

    user_dict = get_user_by_id(user_id)
    return convert_user(user_dict)
