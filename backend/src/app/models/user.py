from app.models.bot import get_bot_by_id, convert_bot
from app.schemas.user import AccountType, UserModel
from fastapi import HTTPException, status
from database.main import MongoDB, User
from bson import ObjectId
from typing import Any


def get_user_by_id(user_id: str) -> dict[str, Any]:
    """
    Retrieves a user from the database by their ID.
    Raises an error if the user does not exist.
    """

    db = MongoDB()
    users_collection = User(db)
    user = users_collection.get_user_by_id(ObjectId(user_id))

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

    user_dict["bots"] = [convert_bot(get_bot_by_id(bot_id)) for bot_id in bots]

    return UserModel(**user_dict)


def get_all_users() -> list[UserModel]:
    """
    Retrieves all users from the database
    """

    db = MongoDB()
    users: list[dict[str, Any]] = db.get_all_users()

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
            detail=f"User {username} already exists",
        )

    db = MongoDB()
    users_collection = User(db)
    user_id: ObjectId = users_collection.create_user(username, password, "standard")
    new_user: dict[str, Any] = get_user_by_id(str(user_id))

    return new_user


def update_user_type(user_id: str, account_type: AccountType) -> UserModel:
    """
    Updates a user's account type.
    Returns the updated user.
    Raises an error if the given account type is invalid.
    """

    if account_type is AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update user to admin.",
        )

    # db = MongoDB()
    # users_collection = User(db)
    # users_collection.update_user_type(user_id, account_type)  TODO: Implement in db

    return convert_user(get_user_by_id(user_id))
