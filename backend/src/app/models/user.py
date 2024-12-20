from database.main import MongoDB, User
from app.schemas.user import UserModel
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
    return users_collection.get_user_by_id(user_id)


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


def get_all_users() -> list[UserModel]:
    """
    Retrieves all users from the database
    """

    db = MongoDB()
    users: list[dict[str, Any]] = db.get_all_users()

    result: list[UserModel] = []
    for user in users:
        user.pop("bots")
        result.append(UserModel(**user))

    return result
