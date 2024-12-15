from app.schemas.user import DBUser, AccountType
from database.main import MongoDB, User


def get_user_by_username(username: str | None = None) -> DBUser | None:
    if username is None:
        return None

    db = MongoDB()
    users = User(db)
    user = users.get_user_by_username(username)

    if user is None:
        return None

    return DBUser(
        id=str(user["_id"]),
        username=str(user["username"]),
        password_hash=str(user["password_hash"]),
        account_type=AccountType(user["account_type"]),
        is_banned=bool(user["is_banned"]),
    )
