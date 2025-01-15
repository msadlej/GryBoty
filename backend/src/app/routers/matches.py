from fastapi import APIRouter, HTTPException, status, Form
from pyobjectID import PyObjectId

from app.dependencies import UserDependency, PremiumDependency
from app.schemas.match import MatchModel, MatchCreate
from app.utils.database import get_db_connection
from app.schemas.bot import BotModel
from app.models.tournament import (
    check_tournament_creator,
    check_tournament_access,
    get_tournament_by_id,
    convert_tournament,
    get_matches_by_tournament,
)
from app.models.match import (
    get_match_by_id,
    convert_match,
    get_bots_by_match_id,
    process_match,
    insert_match,
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
    with get_db_connection() as db:
        if not check_tournament_access(db, current_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        matches = get_matches_by_tournament(db, tournament_id)

    return matches


@router.post(
    "/",
    response_model=MatchModel,
)
async def create_match(
    current_user: PremiumDependency,
    tournament_id: PyObjectId,
    match_data: MatchCreate = Form(...),
):
    with get_db_connection() as db:
        if not check_tournament_creator(db, current_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to create a match.",
            )

        match = insert_match(db, tournament_id, match_data)

    return match


@router.get(
    "/{match_id}/",
    response_model=MatchModel,
)
async def read_match_by_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
    match_id: PyObjectId,
):
    with get_db_connection() as db:
        if not check_tournament_access(db, current_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Match: {match_id} not found.",
            )

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
    with get_db_connection() as db:
        if not check_tournament_access(db, current_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Match: {match_id} not found.",
            )

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
    with get_db_connection() as db:
        if not check_tournament_creator(db, current_user, tournament_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have access to run this match.",
            )

        tournament_dict = get_tournament_by_id(db, tournament_id)
        tournament = convert_tournament(db, tournament_dict, detail=True)

        match_dict = get_match_by_id(db, match_id)
        match = convert_match(db, match_dict, detail=True)

        result = process_match(db, tournament, match)

    return result
