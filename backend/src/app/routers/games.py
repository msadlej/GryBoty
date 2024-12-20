from app.utils.authentication import get_current_active_user
from app.models.game import get_all_game_types
from fastapi import APIRouter, Depends
from app.schemas.game import GameModel
from app.schemas.user import UserModel


router = APIRouter(prefix="/games")


@router.get("/", response_model=list[GameModel])
def read_all_game_types(current_user: UserModel = Depends(get_current_active_user)):
    return get_all_game_types()
