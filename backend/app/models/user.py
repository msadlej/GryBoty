from app.schemas.user import DBUser, AccountType
from typing import Any


fake_users_db = {
    "1": {
        "id": "1",
        "username": "admin",
        "hashed_password": "$2b$12$/m9RMY8pH5fGVVUxDHIBAeVzTWPHBkBBYl/QFur9zfKNE/TqWKXgu",
        "account_type": AccountType.ADMIN,
        "disabled": False,
    },
    "2": {
        "id": "2",
        "username": "smakuch",
        "hashed_password": "$2b$12$dTujJVqHwkratt5lpjQcFuitlGA.IIvaMfFRX.OPjNCqwPGgxeN7K",
        "account_type": AccountType.PREMIUM,
        "disabled": False,
    },
    "3": {
        "id": "3",
        "username": "adam",
        "hashed_password": "$2b$12$uuWqsA3vHi0smAk4LDVOS.LJiMfTn1S0Dvp2LPOYF4heiwoNv1xgO",
        "account_type": AccountType.BASIC,
        "disabled": False,
    },
    "4": {
        "id": "4",
        "username": "jakub",
        "hashed_password": "$2b$12$QyMt0LGYTvnM4kYPcGSV5uViMaEW/UvQXAZ5qk0iJn7d9XhxWU5Oq",
        "account_type": AccountType.BASIC,
        "disabled": True,
    },
}


def get_db_user_by_username(username: str | None) -> DBUser | None:
    if username is None:
        return None

    for id in fake_users_db:
        if fake_users_db[id]["username"] == username:
            user_dict: dict[str, Any] = fake_users_db[id]
            return DBUser(
                id=id,
                hashed_password=user_dict["hashed_password"],
                username=user_dict["username"],
                account_type=user_dict["account_type"],
                disabled=user_dict["disabled"],
            )

    return None
