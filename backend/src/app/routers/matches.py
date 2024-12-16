from app.models.match import get_matches_by_tournament, get_match_by_id
from app.utils.authentication import get_current_active_user
from app.schemas.match import MatchModel
from fastapi import APIRouter, Depends
from app.schemas.user import UserModel
from typing import Annotated


router = APIRouter()


@router.get("/tournaments/{tournament_id}/matches")
async def read_matches_by_tournament_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    matches: list[MatchModel] | None = get_matches_by_tournament(
        current_user, tournament_id
    )

    if matches is None:
        return {"detail": "No matches found."}
    return matches


@router.get("/matches/{match_id}")
async def read_match_by_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    match_id: str,
):
    match: MatchModel | None = get_match_by_id(match_id)

    if match is None:
        return {"detail": "Match not found."}
    return match
