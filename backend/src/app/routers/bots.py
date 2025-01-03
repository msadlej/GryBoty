from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from app.models.bot import insert_bot, update_bot
from app.schemas.bot import BotModel, BotUpdate
from app.dependencies import UserDependency
from pyobjectID import PyObjectId
from app.models.bot import (
    check_bot_access,
    get_bot_by_id,
    convert_bot,
    get_bots_by_user_id,
)


router = APIRouter(prefix="/bots")


@router.get("/", response_model=list[BotModel])
async def read_own_bots(
    current_user: UserDependency,
):
    return get_bots_by_user_id(current_user.id)


@router.post("/", response_model=BotModel)
async def create_bot(
    current_user: UserDependency,
    name: str = Form(min_length=3, max_length=16),
    game_type: PyObjectId = Form(...),
    code: UploadFile = File(...),
):
    new_bot = insert_bot(current_user, name, game_type)

    return new_bot


@router.put("/{bot_id}", response_model=BotModel)
async def edit_bot_by_id(
    current_user: UserDependency,
    bot_id: PyObjectId,
    bot_data: BotUpdate = Form(...),
):
    if not check_bot_access(current_user, bot_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot: {bot_id} not found.",
        )

    updated_bot = update_bot(bot_id, bot_data)

    return updated_bot


@router.get("/{bot_id}", response_model=BotModel)
async def read_bot_by_id(
    current_user: UserDependency,
    bot_id: PyObjectId,
):
    if not check_bot_access(current_user, bot_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot: {bot_id} not found.",
        )

    return convert_bot(get_bot_by_id(bot_id), detail=True)
