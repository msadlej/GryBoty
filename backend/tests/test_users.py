from app.schemas.user import Token, TokenData, AccountType, UserModel
from app.models.user import convert_user
from bson import ObjectId
import pytest


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

    assert standard_account == AccountType.STANDARD
    assert premium_account == AccountType.PREMIUM
    assert admin_account == AccountType.ADMIN

    with pytest.raises(ValueError):
        AccountType("invalid")


def test_user(user_dict):
    user = UserModel(**user_dict)

    assert ObjectId(user.id) == user_dict["_id"]
    assert user.username == "username"
    assert user.account_type == AccountType.STANDARD
    assert user.bots == user_dict["bots"]
    assert user.is_banned


def test_convert_user(user_dict):
    user = convert_user(user_dict, detail=False)

    assert user.bots is None
