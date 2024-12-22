from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from app.models.tournament import get_all_tournaments
from app.schemas.user import AccountType, UserModel
from app.schemas.tournament import TournamentModel
from app.models.user import get_all_users
from app.models.bot import get_all_bots
from app.schemas.bot import BotModel


router = APIRouter()


@router.get("/admin/users/", response_model=list[UserModel])
async def read_all_users(current_user: UserModel = Depends(get_current_active_user)):
    if current_user.account_type != AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return get_all_users()


@router.get("/admin/tournaments/", response_model=list[TournamentModel])
async def read_all_tournaments(
    current_user: UserModel = Depends(get_current_active_user),
):
    if current_user.account_type != AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return get_all_tournaments()


@router.get("/admin/bots/", response_model=list[BotModel])
async def read_all_bots(current_user: UserModel = Depends(get_current_active_user)):
    if current_user.account_type != AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Admins only."
        )

    return get_all_bots()
