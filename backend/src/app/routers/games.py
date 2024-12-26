from app.models.game import get_all_game_types
from app.dependencies import UserDependency
from app.schemas.game import GameModel
from fastapi import APIRouter


router = APIRouter(prefix="/games")


@router.get("/", response_model=list[GameModel])
def read_all_game_types(current_user: UserDependency):
    return get_all_game_types()
