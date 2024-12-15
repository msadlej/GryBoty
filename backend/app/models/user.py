from app.schemas.user import DBUser, AccountType


users_collection = [
    {
        "_id": "1",
        "username": "admin",
        "password_hash": "$2b$12$/m9RMY8pH5fGVVUxDHIBAeVzTWPHBkBBYl/QFur9zfKNE/TqWKXgu",
        "account_type": AccountType.ADMIN,
        "is_banned": False,
    },
    {
        "_id": "2",
        "username": "smakuch",
        "password_hash": "$2b$12$dTujJVqHwkratt5lpjQcFuitlGA.IIvaMfFRX.OPjNCqwPGgxeN7K",
        "account_type": AccountType.PREMIUM,
        "is_banned": False,
    },
    {
        "_id": "3",
        "username": "adam",
        "password_hash": "$2b$12$uuWqsA3vHi0smAk4LDVOS.LJiMfTn1S0Dvp2LPOYF4heiwoNv1xgO",
        "account_type": AccountType.BASIC,
        "is_banned": False,
    },
    {
        "_id": "4",
        "username": "jakub",
        "password_hash": "$2b$12$QyMt0LGYTvnM4kYPcGSV5uViMaEW/UvQXAZ5qk0iJn7d9XhxWU5Oq",
        "account_type": AccountType.BASIC,
        "is_banned": True,
    },
]


def get_user_by_username(username: str | None) -> DBUser | None:
    if username is None:
        return None

    for user in users_collection:
        if user["username"] == username:
            return DBUser(
                _id=str(user["_id"]),
                username=str(user["username"]),
                password_hash=str(user["password_hash"]),
                account_type=AccountType(user["account_type"]),
                is_banned=bool(user["is_banned"]),
            )

    return None
