from fastapi import HTTPException
import pytest

from app.schemas.user import Token, TokenData, AccountType, User
from app.models.user import DBUser


def test_token():
    token = Token(**{"access_token": "string", "token_type": "string"})
    assert token.access_token == "string"
    assert token.token_type == "string"

    token_data = TokenData(username="string")
    assert token_data.username == "string"


def test_account_type():
    standard_account = AccountType("standard")
    premium_account = AccountType("premium")
    admin_account = AccountType("admin")

    assert standard_account is AccountType.STANDARD
    assert premium_account is AccountType.PREMIUM
    assert admin_account is AccountType.ADMIN

    with pytest.raises(ValueError):
        AccountType("invalid")


def test_user_schema(user_dict):
    user = User(**user_dict)

    assert user.id == user_dict["_id"]
    assert user.username == "username"
    assert user.account_type is AccountType.STANDARD
    assert not user.is_banned


class TestUserModel:
    def test_init_data(self, db_connection, user_dict):
        db_user = DBUser(db_connection, data=user_dict)

        assert db_user.id == user_dict["_id"]
        assert db_user.username == "username"
        assert db_user.password_hash == user_dict["password_hash"]
        assert db_user.account_type == "standard"
        assert db_user.bots == user_dict["bots"]
        assert not db_user.is_banned

    def test_init_id(self, db_connection, user_dict):
        with pytest.raises(HTTPException):
            _ = DBUser(db_connection, id=user_dict["_id"])

    def test_to_schema(self, db_connection, user_dict):
        db_user = DBUser(db_connection, data=user_dict)
        user = User(**user_dict)

        assert db_user.to_schema() == user

    def test_insert(self, insert_user, user_dict):
        db_user = insert_user

        assert db_user.username == user_dict["username"]
        assert db_user.password_hash == user_dict["password_hash"]
        assert db_user.account_type == "standard"
        assert db_user.bots == []
        assert not db_user.is_banned
