from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from typing import Any
import jwt

from app.schemas.user import User, UserCreate, PasswordUpdate
from app.models.user import DBUser
from database.main import MongoDB
from app.config import settings


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


def authenticate_user(db: MongoDB, username: str, password: str) -> User | None:
    """
    Authenticate the user with the password.
    Returns None if the user is not found or the password is incorrect.
    """

    user_id = DBUser.get_id_by_username(db, username)
    if user_id is None:
        return None

    db_user = DBUser(db, id=user_id)
    if not verify_password(password, db_user.password_hash):
        return None

    return db_user.to_schema()


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


def create_user(db: MongoDB, user_data: UserCreate) -> User:
    """
    Create a new user.
    Returns the new user.
    """

    hashed_password = get_password_hash(user_data.password)
    db_user = DBUser.insert(db, user_data.username, hashed_password)

    return db_user.to_schema()


def change_user_password(
    db: MongoDB, current_user: User, password_data: PasswordUpdate
) -> User:
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
    db_user = DBUser(db, id=current_user.id)
    db_user.update_password(hashed_password)

    return db_user.to_schema()
