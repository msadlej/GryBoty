from app.schemas.tournament import TournamentModel
from database.main import MongoDB, Tournament
from app.schemas.user import UserModel
from bson import ObjectId
from typing import Any


def get_tournaments_by_creator(creator: UserModel) -> list[TournamentModel] | None:
    db = MongoDB()
    tournaments = Tournament(db)
    tournaments_by_creator: list[dict[str, Any]] = (
        tournaments.get_tournaments_by_creator(ObjectId(creator.id))
    )

    if not tournaments_by_creator:
        return None

    return [
        TournamentModel(
            id=str(tournament["_id"]),
            name=str(tournament["name"]),
            description=str(tournament["description"]),
            game_type=str(tournament["game_type"]),
            creator=str(tournament["creator"]),
            start_date=str(tournament["start_date"]),
            access_code=str(tournament["access_code"]),
            max_participants=int(tournament["max_participants"]),
            participants=[
                str(participant) for participant in tournament["participants"]
            ],
            matches=[str(match) for match in tournament["matches"]],
        )
        for tournament in tournaments_by_creator
    ]


def check_tournament_access(
    current_user: UserModel, tournament: dict[str, Any]
) -> bool:
    is_creator: bool = current_user.id == str(tournament["creator"])
    is_participant: bool = any(
        str(bot_id) in current_user.bots for bot_id in tournament["participants"]
    )

    return is_creator or is_participant


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

    return TournamentModel(
        id=str(tournament["_id"]),
        name=str(tournament["name"]),
        description=str(tournament["description"]),
        game_type=str(tournament["game_type"]),
        creator=str(tournament["creator"]),
        start_date=str(tournament["start_date"]),
        access_code=str(tournament["access_code"]),
        max_participants=int(tournament["max_participants"]),
        participants=[str(participant) for participant in tournament["participants"]],
        matches=[str(match) for match in tournament["matches"]],
    )
