from fastapi import APIRouter, HTTPException, status, Form
from pyobjectID import PyObjectId

from app.schemas.tournament import Tournament, TournamentCreate, TournamentUpdate
from app.dependencies import UserDependency, PremiumDependency
from app.utils.database import get_db_connection
from app.models.tournament import DBTournament
from app.schemas.bot import Bot


router = APIRouter(prefix="/tournaments")


@router.get("/", response_model=list[Tournament])
async def read_own_tournaments(
    current_user: UserDependency,
):
    with get_db_connection() as db:
        tournaments = DBTournament.get_by_user_id(db, current_user.id)

    return tournaments


@router.post("/", response_model=Tournament)
async def create_tournament(
    current_premium_user: PremiumDependency,
    tournament: TournamentCreate = Form(...),
):
    with get_db_connection() as db:
        db_tournament = DBTournament.insert(db, current_premium_user, tournament)
        new_tournament = db_tournament.to_schema()

    return new_tournament


@router.get("/join/{access_code}/", response_model=Tournament)
async def read_tournament_by_access_code(
    current_user: UserDependency,
    access_code: str,
):
    with get_db_connection() as db:
        tournament_id = DBTournament.get_id_by_access_code(db, access_code)

        if tournament_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament with access code: {access_code} not found.",
            )

        db_tournament = DBTournament(db, id=tournament_id)
        tournament = db_tournament.to_schema()

    return tournament


@router.put("/join/{access_code}/", response_model=Tournament)
async def join_tournament(
    current_user: UserDependency,
    access_code: str,
    bot_id: PyObjectId = Form(...),
):
    with get_db_connection() as db:
        tournament_id = DBTournament.get_id_by_access_code(db, access_code)

        if tournament_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament with access code: {access_code} not found.",
            )

        db_tournament = DBTournament(db, id=tournament_id)
        db_tournament.add_participant(bot_id)
        tournament = db_tournament.to_schema()

    return tournament


@router.get("/{tournament_id}/", response_model=Tournament)
async def read_tournament_by_id(
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

        tournament = db_tournament.to_schema()

    return tournament


@router.put("/{tournament_id}/", response_model=Tournament)
async def edit_tournament_by_id(
    current_premium_user: PremiumDependency,
    tournament_id: PyObjectId,
    tournament_data: TournamentUpdate = Form(...),
):
    with get_db_connection() as db:
        db_tournament = DBTournament(db, id=tournament_id)
        if not db_tournament.check_creator(current_premium_user):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        db_tournament.update(tournament_data)
        tournament = db_tournament.to_schema()

    return tournament


@router.get(
    "/{tournament_id}/bots/",
    response_model=list[Bot],
)
async def read_bots_by_tournament_id(
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

        bots = db_tournament.get_participants()

    return bots
