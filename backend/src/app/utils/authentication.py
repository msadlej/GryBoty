from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt

from app.schemas.user import UserModel, UserCreate, PasswordUpdate
from database.main import MongoDB
from app.config import settings
from app.models.user import (
    get_user_by_username,
    convert_user,
    insert_user,
    update_user_password,
)


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


def authenticate_user(db: MongoDB, username: str, password: str) -> UserModel | None:
    """
    Authenticate the user with the password.
    Returns None if the user is not found or the password is incorrect.
    """

    user = get_user_by_username(db, username)
    if user is None or not verify_password(password, user["password_hash"]):
        return None

    return convert_user(db, user)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Create the access token.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc)

    if expires_delta is not None:
        expire += expires_delta
    else:
        expire += timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_user(db: MongoDB, user_data: UserCreate) -> UserModel:
    """
    Create a new user.
    Returns the new user.
    """

    hashed_password = get_password_hash(user_data.password)
    user_dict = insert_user(db, user_data.username, hashed_password)

    return convert_user(db, user_dict)


def change_user_password(
    db: MongoDB, current_user: UserModel, password_data: PasswordUpdate
) -> UserModel:
    """
    Updates a user's password.
    Returns the updated user.
    """

    if authenticate_user(db, current_user.username, password_data.old_password) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hashed_password = get_password_hash(password_data.new_password)
    user_dict = update_user_password(db, current_user.id, hashed_password)

    return convert_user(db, user_dict)
