from app.utils.authentication import get_password_hash
from app.schemas.user import UserModel, AccountType
from bson import ObjectId
import pytest


@pytest.fixture
def patch_get_user_by_username(monkeypatch):
    def mock_get(username: str | None) -> UserModel | None:
        return (
            UserModel(
                **{
                    "_id": ObjectId(),
                    "username": "username",
                    "password_hash": get_password_hash("password"),
                    "account_type": AccountType.ADMIN,
                    "bots": [],
                    "is_banned": False,
                }
            )
            if username == "username"
            else None
        )

    monkeypatch.setattr("app.utils.authentication.get_user_by_username", mock_get)
