from app.schemas.user import Token, TokenData, AccountType, UserModel
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


@pytest.mark.filterwarnings("ignore:`__get_validators__` is deprecated")
def test_user():
    user_dict = {
        "_id": ObjectId(),
        "username": "username",
        "password_hash": "password_hash",
        "account_type": "standard",
        "bots": [ObjectId()],
        "is_banned": True,
    }

    user = UserModel(**user_dict)

    assert user.username == "username"
    assert user.password_hash == "password_hash"
    assert user.account_type == AccountType.STANDARD
    assert user.bots
    assert user.is_banned
