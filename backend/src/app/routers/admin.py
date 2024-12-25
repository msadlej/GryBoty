from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from app.models.tournament import get_all_tournaments
from app.schemas.user import AccountType, UserModel
from app.schemas.tournament import TournamentModel
from app.models.bot import get_all_bots
from app.schemas.bot import BotModel
from app.models.user import (
    get_user_by_id,
    convert_user,
    get_all_users,
    update_user_type,
    ban_user_by_id,
)


router = APIRouter(prefix="/admin")


@router.get("/users/", response_model=list[UserModel])
async def read_all_users(current_user: UserModel = Depends(get_current_active_user)):
    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return get_all_users()


@router.get("/users/{user_id}/", response_model=UserModel)
async def read_user_by_id(
    user_id: str, current_user: UserModel = Depends(get_current_active_user)
):
    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return convert_user(get_user_by_id(user_id))


@router.put("/users/{user_id}/", response_model=UserModel)
async def change_user_account_type(
    user_id: str,
    account_type: AccountType,
    current_user: UserModel = Depends(get_current_active_user),
):
    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return update_user_type(user_id, account_type)


@router.put("/users/{user_id}/ban", response_model=UserModel)
async def ban_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_active_user),
):
    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return ban_user_by_id(user_id)


@router.get("/tournaments/", response_model=list[TournamentModel])
async def read_all_tournaments(
    current_user: UserModel = Depends(get_current_active_user),
):
    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return get_all_tournaments()


@router.get("/bots/", response_model=list[BotModel])
async def read_all_bots(current_user: UserModel = Depends(get_current_active_user)):
    if current_user.account_type is not AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return get_all_bots()
