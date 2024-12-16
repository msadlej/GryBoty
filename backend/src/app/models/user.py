from database.main import MongoDB, User
from app.schemas.user import UserModel


def get_user_by_username(username: str | None = None) -> UserModel | None:
    if username is None:
        return None

    db = MongoDB()
    users = User(db)
    user = users.get_user_by_username(username)

    if user is None:
        return None

    return UserModel(**user)
