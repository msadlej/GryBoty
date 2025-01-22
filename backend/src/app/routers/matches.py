from fastapi import APIRouter, HTTPException, status, Query
from pyobjectID import PyObjectId

from app.dependencies import UserDependency, PremiumDependency
from app.utils.database import get_db_connection
from app.schemas.match import Match, MatchCreate
from app.models.tournament import DBTournament
from app.models.match import DBMatch
from app.schemas.bot import Bot


router = APIRouter(prefix="/tournaments/{tournament_id}/matches")


@router.get(
    "/",
    response_model=list[Match],
)
async def read_matches_by_tournament_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
):
    with get_db_connection() as db:
        db_tournament = DBTournament(db, id=tournament_id)
        if not db_tournament.check_access(current_user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        matches = db_tournament.get_matches()

    return matches


@router.post(
    "/",
    response_model=Match,
)
async def create_match(
    current_user: PremiumDependency,
    tournament_id: PyObjectId,
    match_data: MatchCreate = Query(...),
):
    with get_db_connection() as db:
        db_tournament = DBTournament(db, id=tournament_id)
        if not db_tournament.check_creator(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have access to create a match in tournament: {tournament_id}.",
            )

        db_match = DBMatch.insert(db, tournament_id, match_data)
        match = db_match.to_schema()

    return match


@router.get(
    "/{match_id}/",
    response_model=Match,
)
async def read_match_by_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
    match_id: PyObjectId,
):
    with get_db_connection() as db:
        db_tournament = DBTournament(db, id=tournament_id)
        if not db_tournament.check_access(current_user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        db_match = DBMatch(db, id=match_id)
        match = db_match.to_schema(detail=True)

    return match


@router.get(
    "/{match_id}/bots/",
    response_model=tuple[Bot, Bot],
)
async def read_bots_by_match_id(
    current_user: UserDependency,
    tournament_id: PyObjectId,
    match_id: PyObjectId,
):
    with get_db_connection() as db:
        db_tournament = DBTournament(db, id=tournament_id)
        if not db_tournament.check_access(current_user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        db_match = DBMatch(db, id=match_id)
        bots = db_match.get_players()

    return bots


@router.put(
    "/{match_id}/run/",
    response_model=dict[str, Bot],
)
async def run_match(
    current_user: UserDependency,
    tournament_id: PyObjectId,
    match_id: PyObjectId,
):
    with get_db_connection() as db:
        db_tournament = DBTournament(db, id=tournament_id)
        if not db_tournament.check_creator(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have access to run match: {match_id}.",
            )

        db_match = DBMatch(db, id=match_id)
        result = db_match.run()

    return result
