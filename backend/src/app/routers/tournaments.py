from app.utils.authentication import get_current_active_user
from app.models.tournament import get_tournaments_by_creator
from fastapi import APIRouter, Depends
from app.schemas.user import UserModel
from typing import Annotated


router = APIRouter()


@router.get("/tournaments/")
async def read_own_tournaments(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return get_tournaments_by_creator(current_user)
