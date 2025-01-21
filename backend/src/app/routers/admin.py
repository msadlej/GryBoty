from fastapi import APIRouter, Form
from pyobjectID import PyObjectId

from app.schemas.game_type import GameType, GameTypeCreate
from app.utils.database import get_db_connection
from app.models.tournament import DBTournament
from app.schemas.user import User, UserUpdate
from app.schemas.tournament import Tournament
from app.dependencies import AdminDependency
from app.models.game_type import DBGameType
from app.models.user import DBUser
from app.models.bot import DBBot
from app.schemas.bot import Bot


router = APIRouter(prefix="/admin")


@router.get("/users/", response_model=list[User])
async def read_all_users(current_admin: AdminDependency):
    with get_db_connection() as db:
        users = DBUser.get_all(db)

    return users


@router.get("/users/{user_id}/", response_model=User)
async def read_user_by_id(current_admin: AdminDependency, user_id: PyObjectId):
    with get_db_connection() as db:
        db_user = DBUser(db, id=user_id)
        user = db_user.to_schema()

    return user


@router.put("/users/{user_id}/", response_model=User)
async def edit_user_by_id(
    current_admin: AdminDependency,
    user_id: PyObjectId,
    user_data: UserUpdate = Form(...),
):
    with get_db_connection() as db:
        db_user = DBUser(db, id=user_id)
        db_user.update(user_data)
        user = db_user.to_schema()

    return user


@router.get("/users/{user_id}/bots/", response_model=list[Bot])
async def read_users_bots(
    current_admin: AdminDependency,
    user_id: PyObjectId,
):
    with get_db_connection() as db:
        db_user = DBUser(db, id=user_id)
        bots = db_user.get_bots()

    return bots


@router.get("/users/{user_id}/tournaments/", response_model=list[Tournament])
async def read_users_tournaments(
    current_admin: AdminDependency,
    user_id: PyObjectId,
):
    with get_db_connection() as db:
        db_user = DBUser(db, id=user_id)
        tournaments = db_user.get_tournaments()

    return tournaments


@router.get("/tournaments/", response_model=list[Tournament])
async def read_all_tournaments(current_admin: AdminDependency):
    with get_db_connection() as db:
        tournaments = DBTournament.get_all(db)

    return tournaments


@router.get("/bots/", response_model=list[Bot])
async def read_all_bots(current_admin: AdminDependency):
    with get_db_connection() as db:
        bots = DBBot.get_all(db)

    return bots


@router.post("/games/", response_model=GameType)
def create_game_type(
    current_admin: AdminDependency, game_type_data: GameTypeCreate = Form(...)
):
    with get_db_connection() as db:
        db_game = DBGameType.insert(db, game_type_data)
        new_game = db_game.to_schema()

    return new_game
