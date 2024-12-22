from app.utils.authentication import authenticate_user, create_access_token, create_user
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import Token, UserModel, UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_current_active_user


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

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@router.post("/register", response_model=UserModel)
async def register_user(user_data: UserCreate):
    user: UserModel | None = create_user(user_data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user_data.username} already exists",
        )

    return user
