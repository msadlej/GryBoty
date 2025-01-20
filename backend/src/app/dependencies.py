from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from typing import Annotated, Any
import jwt

from app.schemas.user import TokenData, AccountType, User
from app.utils.database import get_db_connection
from app.models.user import DBUser
from app.config import settings


oauth2_scheme = settings.oauth2_scheme


async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    """
    Get the token data from the token.
    """

    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

        return TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception


async def get_current_user(
    token_data: Annotated[TokenData, Depends(get_token_data)]
) -> User:
    """
    Get the current user from the token data.
    """

    with get_db_connection() as db:
        user_id = DBUser.get_id_by_username(db, token_data.username)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        db_user = DBUser(db, id=user_id)
        user = db_user.to_schema()

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Get the current active user.
    Raises an exception if the user is inactive.
    """

    if current_user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return current_user


async def get_current_premium_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Get the current active premium user.
    Raises an exception if the user is not a premium user.
    """

    if current_user.account_type not in (AccountType.PREMIUM, AccountType.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Premium users only.",
        )

    return current_user


async def get_current_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get the current admin.
    Raises an exception if the user is not an admin.
    """

    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return current_user


UserDependency = Annotated[User, Depends(get_current_active_user)]
AdminDependency = Annotated[User, Depends(get_current_admin)]
PremiumDependency = Annotated[User, Depends(get_current_premium_user)]
