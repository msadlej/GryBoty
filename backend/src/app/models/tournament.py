from app.schemas.user import UserModel, AccountType
from app.schemas.tournament import TournamentModel
from database.main import MongoDB, Tournament
from bson import ObjectId
from typing import Any


def get_own_tournaments(current_user: UserModel) -> list[TournamentModel]:
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
    is_admin: bool = current_user.account_type == AccountType.ADMIN
    is_creator: bool = ObjectId(current_user.id) == tournament["creator"]
    is_participant: bool = any(
        ObjectId(bot_id) in tournament["participants"] for bot_id in current_user.bots
    )

    return any((is_admin, is_creator, is_participant))


def get_tournament_by_id(
    current_user: UserModel, tournament_id: str
) -> TournamentModel | None:
    db = MongoDB()
    tournaments = Tournament(db)
    tournament: dict[str, Any] | None = tournaments.get_tournament_by_id(
        ObjectId(tournament_id)
    )

    if tournament is None or not check_tournament_access(current_user, tournament):
        return None

    return TournamentModel(**tournament)


def get_all_tournaments() -> list[TournamentModel]:
    db = MongoDB()
    tournaments = Tournament(db)
    all_tournaments: list[dict[str, Any]] = tournaments.get_all_tournaments()

    return [TournamentModel(**tournament) for tournament in all_tournaments]
