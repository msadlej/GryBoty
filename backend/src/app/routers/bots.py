from app.models.bot import get_own_bots, get_bot_by_id
from app.utils.authentication import get_current_active_user
from app.schemas.bot import BotModel
from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from app.schemas.user import UserModel
from typing import Annotated


router = APIRouter(prefix="/bots")


@router.get("/", response_model=list[BotModel])
async def read_own_bots(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return get_own_bots(current_user)


@router.get("/{bot_id}", response_model=BotModel)
async def read_bot_by_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    bot_id: str,
):
    bot: BotModel | None = get_bot_by_id(bot_id)

    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot: {bot_id} not found.",
        )

    return bot
