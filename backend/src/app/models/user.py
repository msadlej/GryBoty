from app.schemas.user import UserModel, AccountType
from database.main import MongoDB, User


def get_user_by_username(username: str | None = None) -> UserModel | None:
    if username is None:
        return None

    db = MongoDB()
    users = User(db)
    user = users.get_user_by_username(username)

    if user is None:
        return None

    return UserModel(
        id=str(user["_id"]),
        username=str(user["username"]),
        password_hash=str(user["password_hash"]),
        account_type=AccountType(user["account_type"]),
        bots=[str(bot) for bot in user["bots"]],
        is_banned=bool(user["is_banned"]),
    )
