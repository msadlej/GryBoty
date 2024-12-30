from fastapi import APIRouter, HTTPException, status
from app.dependencies import UserDependency
from app.models.bot import get_bot_by_id
from app.schemas.match import MatchModel
from app.utils.docker import run_game
from app.schemas.bot import BotModel
from typing import Any
from app.models.tournament import (
    check_tournament_creator,
    check_tournament_access,
    get_matches_by_tournament,
)
from app.models.match import (
    get_match_by_id,
    convert_match,
    get_bots_by_match,
    update_match,
    process_logs,
)


router = APIRouter(prefix="/tournaments/{tournament_id}/matches")


@router.get(
    "/",
    response_model=list[MatchModel],
)
async def read_matches_by_tournament_id(
    current_user: UserDependency,
    tournament_id: str,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return get_matches_by_tournament(tournament_id)


@router.get(
    "/{match_id}",
    response_model=MatchModel,
)
async def read_match_by_id(
    current_user: UserDependency,
    tournament_id: str,
    match_id: str,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return convert_match(get_match_by_id(match_id), detail=True)


@router.get(
    "/{match_id}/bots",
    response_model=dict[str, BotModel],
)
async def read_bots_by_match_id(
    current_user: UserDependency,
    tournament_id: str,
    match_id: str,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return get_bots_by_match(match_id)


@router.put(
    "/{match_id}/run",
    response_model=dict[str, BotModel],
)
async def run_match(
    current_user: UserDependency,
    tournament_id: str,
    match_id: str,
):
    if not check_tournament_creator(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to run this match.",
        )

    match: MatchModel = convert_match(get_match_by_id(match_id), detail=True)
    if match.players is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No bots not found for match: {match_id}.",
        )

    bot_1, bot_2 = match.players.values()
    docker_logs: dict[str, Any] | None = run_game(bot_1.code, bot_2.code)
    if docker_logs is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error running Docker commands",
        )

    moves, winner, loser = process_logs(match, docker_logs, bot_1, bot_2)
    if winner is None or loser is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Match: {match_id} ended in a draw.",
        )  # TODO: Update stats after a draw

    return update_match(match, winner, loser, moves)
