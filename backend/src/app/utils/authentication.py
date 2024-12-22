from app.models.user import get_user_by_username, convert_user, insert_user
from datetime import datetime, timedelta, timezone
from app.schemas.user import UserModel, UserCreate
from typing import Any
from app.config import settings
import jwt


pwd_context = settings.pwd_context


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the plain password against the hashed password.
    """

    result: bool = pwd_context.verify(plain_password, hashed_password)
    return result


def get_password_hash(password: str) -> str:
    """
    Get the hashed password.
    """

    hashed_password: str = pwd_context.hash(password)
    return hashed_password


def authenticate_user(username: str, password: str) -> UserModel | None:
    """
    Authenticate the user with the password.
    Returns None if the user is not found or the password is incorrect.
    """

    user: dict[str, Any] | None = get_user_by_username(username)

    if user is None or not verify_password(password, user["password_hash"]):
        return None

    return convert_user(user)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Create the access token.
    """

    to_encode: dict[str, Any] = data.copy()
    expire: datetime = datetime.now(timezone.utc)

    if expires_delta is not None:
        expire += expires_delta
    else:
        expire += timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_user(user_data: UserCreate) -> UserModel | None:
    """
    Create a new user.
    """

    hashed_password = get_password_hash(user_data.password)
    user: dict[str, Any] | None = insert_user(user_data.username, hashed_password)

    return convert_user(user) if user is not None else None
