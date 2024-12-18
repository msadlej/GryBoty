from app.models.tournament import get_own_tournaments, get_tournament_by_id
from app.utils.authentication import get_current_active_user
from app.models.match import get_bots_by_tournament
from app.schemas.tournament import TournamentModel
from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from app.schemas.user import UserModel
from app.schemas.bot import BotModel
from typing import Annotated


router = APIRouter(prefix="/tournaments")


@router.get("/", response_model=list[TournamentModel])
async def read_own_tournaments(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return get_own_tournaments(current_user)


@router.get("/{tournament_id}", response_model=TournamentModel)
async def read_tournament_by_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return tournament


@router.get(
    "/{tournament_id}/bots",
    response_model=list[BotModel],
)
async def read_bots_by_tournament_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    bots: list[BotModel] | None = get_bots_by_tournament(current_user, tournament)
    if bots is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No bots found in tournament: {tournament_id}.",
        )

    return bots
