import pytest
from app.schemas.user import (
    Token,
    TokenData,
    AccountType,
    User,
    DBUser,
)


def test_token():
    token = Token(**{"access_token": "string", "token_type": "string"})
    assert token.access_token == "string"
    assert token.token_type == "string"

    token_data = TokenData(username="string")
    assert token_data.username == "string"


def test_account_type():
    basic_account = AccountType("basic")
    premium_account = AccountType("premium")
    admin_account = AccountType("admin")

    assert basic_account == AccountType.BASIC
    assert premium_account == AccountType.PREMIUM
    assert admin_account == AccountType.ADMIN

    with pytest.raises(ValueError):
        AccountType("invalid")


def test_user():
    db_user = DBUser(
        id="id",
        username="username",
        password_hash="password_hash",
        account_type=AccountType("basic"),
        is_banned=True,
    )

    assert db_user.id == "id"
    assert db_user.username == "username"
    assert db_user.password_hash == "password_hash"
    assert db_user.account_type == AccountType.BASIC
    assert db_user.is_banned

    db_user_dict = db_user.model_dump()
    user = User(**db_user_dict)

    assert user.username == "username"
    assert user.account_type == AccountType.BASIC
    assert user.is_banned
