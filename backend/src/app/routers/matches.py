from fastapi import APIRouter, HTTPException, status
from pyobjectID import PyObjectId

from app.utils.database import get_db_connection
from app.dependencies import UserDependency
from app.schemas.match import MatchModel
from app.utils.docker import run_game
from app.schemas.bot import BotModel
from app.models.tournament import (
    check_tournament_creator,
    check_tournament_access,
    get_matches_by_tournament,
)
from app.models.match import (
    get_match_by_id,
    convert_match,
    get_bots_by_match_id,
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
    tournament_id: PyObjectId,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return get_matches_by_tournament(tournament_id)


@router.get(
    "/{match_id}/",
    response_model=MatchModel,
)
async def read_match_by_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
    match_id: PyObjectId,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    with get_db_connection() as db:
        match_dict = get_match_by_id(db, match_id)
        match = convert_match(db, match_dict, detail=True)

    return match


@router.get(
    "/{match_id}/bots/",
    response_model=dict[str, BotModel],
)
async def read_bots_by_match_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
    match_id: PyObjectId,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    with get_db_connection() as db:
        bots = get_bots_by_match_id(db, match_id)

    return bots


@router.put(
    "/{match_id}/run/",
    response_model=dict[str, BotModel],
)
async def run_match(
    current_user: UserDependency,
    tournament_id: PyObjectId,
    match_id: PyObjectId,
):
    if not check_tournament_creator(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to run this match.",
        )

    with get_db_connection() as db:
        match_dict = get_match_by_id(db, match_id)
        match = convert_match(db, match_dict, detail=True)
        if match.players is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bots not found for match: {match_id}.",
            )

        bot_1, bot_2 = match.players.values()
        docker_logs = run_game(bot_1.code_path, bot_2.code_path)
        if docker_logs is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error running Docker commands",
            )

        moves, winner, loser = process_logs(docker_logs, bot_1, bot_2)
        if winner is None or loser is None:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f"Match: {match_id} ended in a draw.",
            )  # TODO: Replay match after a draw

        result = update_match(db, match, winner, loser, moves)

    return result
