from fastapi import APIRouter, HTTPException, status, Form
from pyobjectID import PyObjectId

from app.schemas.tournament import TournamentModel, TournamentCreate, TournamentUpdate
from app.dependencies import UserDependency, PremiumDependency
from app.utils.database import get_db_connection
from app.schemas.bot import BotModel
from app.models.tournament import (
    check_tournament_access,
    check_tournament_creator,
    get_tournament_by_id,
    convert_tournament,
    get_bots_by_tournament,
    get_tournaments_by_user_id,
    get_tournament_id_by_access_code,
    insert_tournament,
    update_tournament,
    add_tournament_participant,
)


router = APIRouter(prefix="/tournaments")


@router.get("/", response_model=list[TournamentModel])
async def read_own_tournaments(
    current_user: UserDependency,
):
    with get_db_connection() as db:
        tournaments = get_tournaments_by_user_id(db, current_user.id)

    return tournaments


@router.post("/", response_model=TournamentModel)
async def create_tournament(
    current_premium_user: PremiumDependency,
    tournament: TournamentCreate = Form(...),
):
    with get_db_connection() as db:
        new_tournament = insert_tournament(db, current_premium_user, tournament)

    return new_tournament


@router.put("/", response_model=TournamentModel)
async def join_tournament(
    current_user: UserDependency,
    access_code: str = Form(...),
    bot_id: PyObjectId = Form(...),
):
    with get_db_connection() as db:
        tournament_id = get_tournament_id_by_access_code(db, access_code)

        if tournament_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Access code: {access_code} not found.",
            )

        tournament = add_tournament_participant(db, tournament_id, bot_id)

    return tournament


@router.get("/{tournament_id}/", response_model=TournamentModel)
async def read_tournament_by_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
):
    with get_db_connection() as db:
        if not check_tournament_access(db, current_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        tournament_dict = get_tournament_by_id(db, tournament_id)
        tournament = convert_tournament(db, tournament_dict, detail=True)

    return tournament


@router.put("/{tournament_id}/", response_model=TournamentModel)
async def edit_tournament_by_id(
    current_premium_user: PremiumDependency,
    tournament_id: PyObjectId,
    tournament_data: TournamentUpdate = Form(...),
):
    with get_db_connection() as db:
        if not check_tournament_creator(db, current_premium_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        tournament = update_tournament(db, tournament_id, tournament_data)

    return tournament


@router.get(
    "/{tournament_id}/bots/",
    response_model=list[BotModel],
)
async def read_bots_by_tournament_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
):
    with get_db_connection() as db:
        if not check_tournament_access(db, current_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        bots = get_bots_by_tournament(db, tournament_id)

    return bots
