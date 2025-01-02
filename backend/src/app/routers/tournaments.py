from app.schemas.tournament import TournamentModel, TournamentCreate, TournamentUpdate
from app.dependencies import UserDependency, PremiumDependency
from fastapi import APIRouter, HTTPException, status, Form
from app.schemas.bot import BotModel
from app.models.tournament import (
    check_tournament_access,
    check_tournament_creator,
    get_tournament_by_id,
    convert_tournament,
    get_bots_by_tournament,
    get_own_tournaments,
    insert_tournament,
    update_tournament,
)


router = APIRouter(prefix="/tournaments")


@router.get("/", response_model=list[TournamentModel])
async def read_own_tournaments(
    current_user: UserDependency,
):
    return get_own_tournaments(current_user)


@router.post("/", response_model=TournamentModel)
async def create_tournament(
    current_premium_user: PremiumDependency,
    tournament: TournamentCreate = Form(...),
):
    return insert_tournament(current_premium_user, tournament)


@router.get("/{tournament_id}", response_model=TournamentModel)
async def read_tournament_by_id(
    current_user: UserDependency,
    tournament_id: str,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return convert_tournament(get_tournament_by_id(tournament_id), detail=True)


@router.put("/{tournament_id}", response_model=TournamentModel)
async def edit_tournament_by_id(
    current_premium_user: PremiumDependency,
    tournament_id: str,
    update: TournamentUpdate = Form(...),
):
    if not check_tournament_creator(current_premium_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return update_tournament(tournament_id, update)


@router.get(
    "/{tournament_id}/bots",
    response_model=list[BotModel],
)
async def read_bots_by_tournament_id(
    current_user: UserDependency,
    tournament_id: str,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return get_bots_by_tournament(tournament_id)
