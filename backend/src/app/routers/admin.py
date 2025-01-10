from fastapi import APIRouter, Form
from pyobjectID import PyObjectId

from app.models.user import get_user_by_id, convert_user, get_all_users, update_user
from app.models.tournament import get_all_tournaments, get_tournaments_by_user_id
from app.models.bot import get_all_bots, get_bots_by_user_id
from app.schemas.user import UserModel, UserUpdate
from app.schemas.tournament import TournamentModel
from app.schemas.game import GameModel, GameCreate
from app.utils.database import get_db_connection
from app.dependencies import AdminDependency
from app.models.game import insert_game_type
from app.schemas.bot import BotModel


router = APIRouter(prefix="/admin")


@router.get("/users/", response_model=list[UserModel])
async def read_all_users(current_admin: AdminDependency):
    return get_all_users()


@router.get("/users/{user_id}/", response_model=UserModel)
async def read_user_by_id(current_admin: AdminDependency, user_id: PyObjectId):
    user_dict = get_user_by_id(user_id)
    return convert_user(user_dict)


@router.put("/users/{user_id}/", response_model=UserModel)
async def edit_user_by_id(
    current_admin: AdminDependency,
    user_id: PyObjectId,
    user_data: UserUpdate = Form(...),
):
    return update_user(user_id, user_data)


@router.get("/users/{user_id}/bots/", response_model=list[BotModel])
async def read_users_bots(
    current_admin: AdminDependency,
    user_id: PyObjectId,
):
    return get_bots_by_user_id(user_id)


@router.get("/users/{user_id}/tournaments/", response_model=list[TournamentModel])
async def read_users_tournaments(
    current_admin: AdminDependency,
    user_id: PyObjectId,
):
    return get_tournaments_by_user_id(user_id)


@router.get("/tournaments/", response_model=list[TournamentModel])
async def read_all_tournaments(current_admin: AdminDependency):
    return get_all_tournaments()


@router.get("/bots/", response_model=list[BotModel])
async def read_all_bots(current_admin: AdminDependency):
    return get_all_bots()


@router.post("/games/", response_model=GameModel)
def create_game_type(current_admin: AdminDependency, game_data: GameCreate = Form(...)):
    with get_db_connection() as db:
        return insert_game_type(db, game_data)
