from app.models.bot import check_bot_access, get_bot_by_id, convert_bot, get_own_bots
from fastapi import APIRouter, HTTPException, status, UploadFile
from app.schemas.bot import BotModel, BotCreate
from app.dependencies import UserDependency
from app.models.bot import insert_bot


router = APIRouter(prefix="/bots")


@router.get("/", response_model=list[BotModel])
async def read_own_bots(
    current_user: UserDependency,
):
    return get_own_bots(current_user)


@router.post("/", response_model=BotModel)
async def create_bot(current_user: UserDependency, bot: BotCreate, code: UploadFile):
    bot = insert_bot(current_user, bot)
    # TODO: Save the file in docker
    return bot


@router.get("/{bot_id}", response_model=BotModel)
async def read_bot_by_id(
    current_user: UserDependency,
    bot_id: str,
):
    if not check_bot_access(current_user, bot_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot: {bot_id} not found.",
        )

    return convert_bot(get_bot_by_id(bot_id), detail=True)
