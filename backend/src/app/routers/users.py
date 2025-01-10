from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import Token, UserModel, UserCreate, PasswordUpdate
from app.dependencies import UserDependency
from app.utils.database import get_db_connection
import app.utils.authentication as auth


router = APIRouter()


@router.post(
    "/token/",
    response_model=Token,
    name="login",
    description="Login for access token",
    summary="User login",
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_db_connection() as db:
        user: UserModel | None = auth.authenticate_user(
            db, form_data.username, form_data.password
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token: str = auth.create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register/", response_model=UserModel)
async def register_user(user_data: UserCreate = Form(...)):
    with get_db_connection() as db:
        new_user = auth.create_user(db, user_data)

    return new_user


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserDependency):
    return current_user


@router.put("/users/change_password/", response_model=UserModel)
async def change_password(
    current_user: UserDependency,
    user_data: PasswordUpdate = Form(...),
):
    with get_db_connection() as db:
        user = auth.change_user_password(db, current_user, user_data)

    return user
