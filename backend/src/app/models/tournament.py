from app.schemas.user import UserModel, AccountType
from app.schemas.tournament import TournamentModel
from database.main import MongoDB, Tournament
from bson import ObjectId
from typing import Any


def check_tournament_creator(current_user: UserModel, tournament_id: str) -> bool:
    """
    Checks if the user is the creator of the tournament or an admin.
    """

    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )
    if tournament is None:
        return False

    is_creator: bool = tournament.creator == current_user.id
    is_admin: bool = current_user.account_type == AccountType.ADMIN

    return is_creator or is_admin


def get_own_tournaments(current_user: UserModel) -> list[TournamentModel]:
    """
    Retrieves all tournaments that the user has created or is participating in.
    """

    db = MongoDB()
    tournaments = Tournament(db)

    own_tournaments: list[dict[str, Any]] = tournaments.get_tournaments_by_creator(
        ObjectId(current_user.id)
    )
    for bot_id in current_user.bots:
        own_tournaments.extend(tournaments.get_tournaments_by_bot_id(ObjectId(bot_id)))

    return [TournamentModel(**tournament) for tournament in own_tournaments]


def check_tournament_access(
    current_user: UserModel, tournament: dict[str, Any]
) -> bool:
    """
    Checks if the user has access to the tournament.
    """

    is_admin: bool = current_user.account_type == AccountType.ADMIN
    is_creator: bool = ObjectId(current_user.id) == tournament["creator"]
    is_participant: bool = any(
        ObjectId(bot_id) in tournament["participants"] for bot_id in current_user.bots
    )

    return any((is_admin, is_creator, is_participant))


def get_tournament_by_id(
    current_user: UserModel, tournament_id: str
) -> TournamentModel | None:
    """
    Retrieves a tournament from the database by its ID.
    Returns None if the tournament does not exist or the user does not have access to it.
    """

    db = MongoDB()
    tournaments = Tournament(db)
    tournament: dict[str, Any] | None = tournaments.get_tournament_by_id(
        ObjectId(tournament_id)
    )

    return (
        TournamentModel(**tournament)
        if tournament is not None and check_tournament_access(current_user, tournament)
        else None
    )


def get_all_tournaments() -> list[TournamentModel]:
    """
    Retrieves all tournaments from the database.
    """

    db = MongoDB()
    tournaments = Tournament(db)
    all_tournaments: list[dict[str, Any]] = tournaments.get_all_tournaments()

    return [TournamentModel(**tournament) for tournament in all_tournaments]
