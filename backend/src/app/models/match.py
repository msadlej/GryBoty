from app.models.tournament import get_tournament_by_id
from app.schemas.tournament import TournamentModel
from database.main import MongoDB, Match
from app.schemas.match import MatchModel
from app.schemas.user import UserModel
from bson import ObjectId
from typing import Any


def get_match_by_id(match_id: str) -> MatchModel | None:
    db = MongoDB()
    matches = Match(db)
    match: dict[str, Any] | None = matches.get_match_by_id(ObjectId(match_id))

    if match is None:
        return None

    return MatchModel(**match)


def get_matches_by_tournament(
    current_user: UserModel, tournament_id: str
) -> list[MatchModel] | None:
    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    if tournament is None:
        return None

    result = [
        match
        for match_id in tournament.matches
        if (match := get_match_by_id(match_id)) is not None
    ]

    if not result:
        return None
    return result
