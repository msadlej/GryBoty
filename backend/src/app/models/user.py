from database.main import MongoDB, User
from app.schemas.user import UserModel
from typing import Any


def get_user_by_username(username: str | None = None) -> UserModel | None:
    """
    Retrieve a user from the database by their username.
    Returns None if the user does not exist.
    """

    if username is None:
        return None

    db = MongoDB()
    users = User(db)
    user = users.get_user_by_username(username)

    if user is None:
        return None

    return UserModel(**user)


def get_all_users() -> list[UserModel]:
    """Retrieve all users from the database"""

    db = MongoDB()
    all_users: list[dict[str, Any]] = db.get_all_users()

    return [UserModel(**user) for user in all_users]
