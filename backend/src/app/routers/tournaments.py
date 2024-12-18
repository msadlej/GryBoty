from app.models.tournament import get_own_tournaments, get_tournament_by_id
from app.utils.authentication import get_current_active_user
from app.schemas.tournament import TournamentModel
from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from app.schemas.user import UserModel
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
