from fastapi import APIRouter

from app.utils.database import get_db_connection
from app.dependencies import UserDependency
from app.models.game_type import DBGameType
from app.schemas.game_type import GameType


router = APIRouter(prefix="/games")


@router.get("/", response_model=list[GameType])
def read_all_game_types(current_user: UserDependency):
    with get_db_connection() as db:
        game_types = DBGameType.get_all(db)

    return game_types
