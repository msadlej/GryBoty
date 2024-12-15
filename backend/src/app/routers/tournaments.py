from app.utils.authentication import get_current_active_user
from fastapi import APIRouter, Depends
from app.schemas.user import User
from typing import Annotated


router = APIRouter()


@router.get("/tournaments/")
async def read_own_tournaments(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [
        {"name": "tournament 1", "owner": current_user.username},
        {"name": "tournament 2", "owner": current_user.username},
    ]
