from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from pyobjectID import PyObjectId

from app.models.bot import insert_bot, update_bot
from app.utils.database import get_db_connection
from app.schemas.bot import BotModel, BotUpdate
from app.dependencies import UserDependency
from app.models.bot import (
    check_bot_access,
    get_bot_by_id,
    get_bots_by_user_id,
    get_bots_by_game_type,
)


router = APIRouter(prefix="/bots")


@router.get("/", response_model=list[BotModel])
async def read_own_bots(
    current_user: UserDependency,
):
    with get_db_connection() as db:
        bot = get_bots_by_user_id(db, current_user.id)

    return bot


@router.post("/", response_model=BotModel)
async def create_bot(
    current_user: UserDependency,
    name: str = Form(min_length=3, max_length=16),
    game_type_id: PyObjectId = Form(...),
    code: UploadFile = File(...),
):
    with get_db_connection() as db:
        new_bot = insert_bot(db, current_user, name, game_type_id, code.file.read())

    return new_bot


@router.put("/{bot_id}/", response_model=BotModel)
async def edit_bot_by_id(
    current_user: UserDependency,
    bot_id: PyObjectId,
    bot_data: BotUpdate = Form(...),
):
    with get_db_connection() as db:
        if not check_bot_access(db, current_user, bot_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bot: {bot_id} not found.",
            )

        updated_bot = update_bot(db, bot_id, bot_data)

    return updated_bot


@router.get("/{bot_id}/", response_model=BotModel)
async def read_bot_by_id(
    current_user: UserDependency,
    bot_id: PyObjectId,
):
    with get_db_connection() as db:
        if not check_bot_access(db, current_user, bot_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bot: {bot_id} not found.",
            )

        bot = get_bot_by_id(db, bot_id)

    return bot
