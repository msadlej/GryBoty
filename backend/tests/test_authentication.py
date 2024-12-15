from app.schemas.user import AccountType
from app.utils.authentication import (
    verify_password,
    get_password_hash,
    authenticate_user,
)


def test_verify_password():
    password = "password"
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password)
    assert not verify_password("wrong_password", hashed_password)


def test_authenticate_user(patch_get_user_by_username):
    user = authenticate_user("username", "password")
    assert user is not None
    assert user.username == "username"
    assert user.account_type == AccountType.ADMIN
    assert user.bots == []
    assert not user.is_banned

    user = authenticate_user("username", "wrong_password")
    assert user is None

    user = authenticate_user("wrong_username", "password")
    assert user is None
