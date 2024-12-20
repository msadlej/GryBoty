from app.models.bot import check_bot_access, get_bot_by_id, convert_bot, get_own_bots
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.authentication import get_current_active_user
from app.schemas.user import UserModel
from app.schemas.bot import BotModel
from typing import Annotated, Any


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
    bot: dict[str, Any] | None = get_bot_by_id(bot_id)

    if bot is None or not check_bot_access(current_user, bot_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot: {bot_id} not found.",
        )

    return convert_bot(bot, detail=True)
