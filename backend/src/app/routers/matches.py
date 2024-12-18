from app.models.match import get_matches_by_tournament, get_match_by_id, update_match
from app.utils.authentication import get_current_active_user
from app.models.tournament import check_tournament_creator
from app.utils.docker import run_game
from fastapi import HTTPException, status
from app.schemas.match import MatchModel
from app.models.bot import get_bot_by_id
from fastapi import APIRouter, Depends
from app.schemas.user import UserModel
from app.schemas.bot import BotModel
from typing import Annotated, Any


router = APIRouter(prefix="/tournaments/{tournament_id}")


@router.get(
    "/matches",
    response_model=list[MatchModel],
)
async def read_matches_by_tournament_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    matches: list[MatchModel] | None = get_matches_by_tournament(
        current_user, tournament_id
    )

    if matches is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return matches


@router.get(
    "/matches/{match_id}",
    response_model=MatchModel,
)
async def read_match_by_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
    match_id: str,
):
    match: MatchModel | None = get_match_by_id(current_user, tournament_id, match_id)

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return match


@router.put(
    "/matches/{match_id}/run",
    response_model=dict[str, BotModel] | None,
)
async def run_match(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
    match_id: str,
):
    match: MatchModel | None = get_match_by_id(current_user, tournament_id, match_id)
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    if not check_tournament_creator(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to run this match.",
        )

    docker_logs: dict[str, Any] | None = run_game()
    if docker_logs is None:
        raise HTTPException(status_code=500, detail="Error running Docker commands")

    result: dict[str, BotModel] | None = update_match(
        current_user, tournament_id, match_id, docker_logs
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Match: {match_id} ended in a draw.",
        )

    return result


@router.get(
    "/matches/{match_id}/bots",
    response_model=dict[str, BotModel | None],
)
async def read_bots_by_match_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
    match_id: str,
):
    match: MatchModel | None = get_match_by_id(current_user, tournament_id, match_id)

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    bot_1: BotModel | None = get_bot_by_id(match.players["bot1"])
    bot_2: BotModel | None = get_bot_by_id(match.players["bot2"])

    return {"bot1": bot_1, "bot2": bot_2}
