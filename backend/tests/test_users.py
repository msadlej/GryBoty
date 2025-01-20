import pytest

from app.schemas.user import Token, TokenData, AccountType, User


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
