from app.models.tournament import get_all_tournaments
from app.schemas.user import AccountType, UserModel
from app.schemas.tournament import TournamentModel
from app.dependencies import AdminDependency
from app.models.bot import get_all_bots
from app.schemas.bot import BotModel
from fastapi import APIRouter
from app.models.user import (
    get_user_by_id,
    convert_user,
    get_all_users,
    update_user_type,
    ban_user_by_id,
)


router = APIRouter(prefix="/admin")


@router.get("/users/", response_model=list[UserModel])
async def read_all_users(current_admin: AdminDependency):
    return get_all_users()


@router.get("/users/{user_id}/", response_model=UserModel)
async def read_user_by_id(current_admin: AdminDependency, user_id: str):
    return convert_user(get_user_by_id(user_id))


@router.put("/users/{user_id}/", response_model=UserModel)
async def change_user_account_type(
    current_admin: AdminDependency,
    user_id: str,
    account_type: AccountType,
):
    return update_user_type(user_id, account_type)


@router.put("/users/{user_id}/ban", response_model=UserModel)
async def ban_user(
    current_admin: AdminDependency,
    user_id: str,
):
    return ban_user_by_id(user_id)


@router.get("/tournaments/", response_model=list[TournamentModel])
async def read_all_tournaments(current_admin: AdminDependency):
    return get_all_tournaments()


@router.get("/bots/", response_model=list[BotModel])
async def read_all_bots(current_admin: AdminDependency):
    return get_all_bots()
