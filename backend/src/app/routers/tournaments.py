from app.schemas.tournament import TournamentModel, TournamentCreate, TournamentUpdate
from app.dependencies import UserDependency, PremiumDependency
from fastapi import APIRouter, HTTPException, status, Form
from app.schemas.bot import BotModel
from pyobjectID import PyObjectId
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
    return get_tournaments_by_user_id(current_user.id)


@router.post("/", response_model=TournamentModel)
async def create_tournament(
    current_premium_user: PremiumDependency,
    tournament: TournamentCreate = Form(...),
):
    return insert_tournament(current_premium_user, tournament)


@router.put("/", response_model=TournamentModel)
async def join_tournament(
    current_user: UserDependency,
    access_code: str = Form(...),
    bot_id: PyObjectId = Form(...),
):
    tournament_id = get_tournament_id_by_access_code(access_code)

    if tournament_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Access code: {access_code} not found.",
        )

    return add_tournament_participant(tournament_id, bot_id)


@router.get("/{tournament_id}", response_model=TournamentModel)
async def read_tournament_by_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    tournament_dict = get_tournament_by_id(tournament_id)
    return convert_tournament(tournament_dict, detail=True)


@router.put("/{tournament_id}", response_model=TournamentModel)
async def edit_tournament_by_id(
    current_premium_user: PremiumDependency,
    tournament_id: PyObjectId,
    tournament_data: TournamentUpdate = Form(...),
):
    if not check_tournament_creator(current_premium_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return update_tournament(tournament_id, tournament_data)


@router.get(
    "/{tournament_id}/bots",
    response_model=list[BotModel],
)
async def read_bots_by_tournament_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return get_bots_by_tournament(tournament_id)
