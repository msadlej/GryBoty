from app.models.tournament import get_tournaments_by_creator, get_tournament_by_id
from app.utils.authentication import get_current_active_user
from app.schemas.tournament import TournamentModel
from fastapi import APIRouter, Depends
from app.schemas.user import UserModel
from typing import Annotated


router = APIRouter()


@router.get("/tournaments/")
async def read_own_tournaments(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    tournaments: list[TournamentModel] | None = get_tournaments_by_creator(current_user)

    if tournaments is None:
        return {"detail": "No tournaments found."}
    return tournaments


@router.get("/tournaments/{tournament_id}")
async def read_tournament_by_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    if tournament is None:
        return {"detail": "Tournament not found."}
    return tournament
