from fastapi import APIRouter

from app.utils.database import get_db_connection
from app.models.game import get_all_game_types
from app.dependencies import UserDependency
from app.schemas.game import GameTypeModel


router = APIRouter(prefix="/games")


@router.get("/", response_model=list[GameTypeModel])
def read_all_game_types(current_user: UserDependency):
    with get_db_connection() as db:
        games = get_all_game_types(db)

    return games
