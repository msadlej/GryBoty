from app.schemas.user import Token, UserModel, UserCreate, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_current_active_user
from typing import Annotated
from app.utils.authentication import (
    authenticate_user,
    create_access_token,
    create_user,
    update_user_password,
)


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: UserModel | None = authenticate_user(form_data.username, form_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token: str = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserModel)
async def register_user(user_data: UserCreate):
    return create_user(user_data)


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)]
):
    return current_user


@router.put("/users/change_password/", response_model=UserModel)
async def change_password(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    user_data: UserUpdate,
):
    return update_user_password(current_user, user_data)
