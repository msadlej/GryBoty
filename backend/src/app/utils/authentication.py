from app.models.user import get_user_by_username, convert_user, insert_user, update_user
from app.schemas.user import UserModel, UserCreate, UserUpdate
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.config import settings
from typing import Any
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


def create_user(user_data: UserCreate) -> UserModel:
    """
    Create a new user.
    Returns the new user.
    """

    hashed_password = get_password_hash(user_data.password)
    user: dict[str, Any] = insert_user(user_data.username, hashed_password)

    return convert_user(user)


def update_user_password(current_user: UserModel, user_data: UserUpdate) -> UserModel:
    """
    Updates a user's password.
    Returns the updated user.
    """

    if authenticate_user(current_user.username, user_data.old_password) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hashed_password = get_password_hash(user_data.new_password)
    user: dict[str, Any] = update_user(current_user.id, hashed_password)

    return convert_user(user)
