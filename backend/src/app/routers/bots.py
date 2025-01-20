from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from pyobjectID import PyObjectId

from app.utils.database import get_db_connection
from app.dependencies import UserDependency
from app.schemas.bot import Bot, BotUpdate
from app.models.bot import DBBot


router = APIRouter(prefix="/bots")


@router.get("/", response_model=list[Bot])
async def read_own_bots(
    current_user: UserDependency,
):
    with get_db_connection() as db:
        bots = DBBot.get_by_user_id(db, current_user.id)

    return bots


@router.post("/", response_model=Bot)
async def create_bot(
    current_user: UserDependency,
    name: str = Form(min_length=3, max_length=16),
    game_type_id: PyObjectId = Form(...),
    code: UploadFile = File(...),
):
    with get_db_connection() as db:
        db_bot = DBBot.insert(db, current_user, name, game_type_id, code.file.read())
        new_bot = db_bot.to_schema()

    return new_bot


@router.get("/{bot_id}/", response_model=Bot)
async def read_bot_by_id(
    current_user: UserDependency,
    bot_id: PyObjectId,
):
    with get_db_connection() as db:
        db_bot = DBBot(db, id=bot_id)

        if not db_bot.check_access(current_user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bot: {bot_id} not found.",
            )

        bot = db_bot.to_schema()

    return bot


@router.put("/{bot_id}/", response_model=Bot)
async def edit_bot_by_id(
    current_user: UserDependency,
    bot_id: PyObjectId,
    bot_data: BotUpdate = Form(...),
):
    with get_db_connection() as db:
        db_bot = DBBot(db, id=bot_id)

        if not db_bot.check_access(current_user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bot: {bot_id} not found.",
            )

        db_bot.update(bot_data)
        updated_bot = db_bot.to_schema()

    return updated_bot


# TODO: Implement in db
# @router.delete("/{bot_id}/")
# async def delete_bot_by_id(
#     current_user: UserDependency,
#     bot_id: PyObjectId,
# ):
#     with get_db_connection() as db:
#         db_bot = DBBot(db, id=bot_id)

#         if not db_bot.check_access(current_user):
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Bot: {bot_id} not found.",
#             )

#         db_bot.delete()
