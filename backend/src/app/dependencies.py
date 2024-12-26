from app.models.user import get_user_by_username, convert_user
from app.schemas.user import TokenData, AccountType, UserModel
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from typing import Annotated, Any
from app.config import settings
import jwt


oauth2_scheme = settings.oauth2_scheme


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
    """
    Get the current user from the token.
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

        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user: dict[str, Any] | None = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception

    return convert_user(user)


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
) -> UserModel:
    """
    Get the current active user.
    Raises an exception if the user is inactive.
    """

    if current_user.is_banned:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_admin(
    current_user: UserModel = Depends(get_current_active_user),
) -> UserModel:
    """
    Get the current admin.
    Raises an exception if the user is not an admin.
    """

    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return current_user


UserDependency = Annotated[UserModel, Depends(get_current_active_user)]
AdminDependency = Annotated[UserModel, Depends(get_current_admin)]
