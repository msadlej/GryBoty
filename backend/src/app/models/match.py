from app.models.tournament import get_tournament_by_id
from app.schemas.tournament import TournamentModel
from database.main import MongoDB, Match, Bot
from app.models.bot import get_bot_by_id
from app.schemas.match import MatchModel
from app.schemas.user import UserModel
from app.schemas.bot import BotModel
from bson import ObjectId
from typing import Any


def get_match_by_id(
    current_user: UserModel, tournament_id: str, match_id: str
) -> MatchModel | None:
    """
    Retrieve a match from the database by its ID.
    Returns None if the match does not exist or the user does not have access to it.
    """

    db = MongoDB()
    matches = Match(db)
    match: dict[str, Any] | None = matches.get_match_by_id(ObjectId(match_id))
    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    if match is None or tournament is None:
        return None

    return MatchModel(**match)


def get_matches_by_tournament(
    current_user: UserModel, tournament_id: str
) -> list[MatchModel] | None:
    """
    Retrieve all matches from the database that belong to a specific tournament.
    Returns None if the tournament does not exist or the user does not have access to it.
    """

    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    if tournament is None:
        return None

    result = [
        match
        for match_id in tournament.matches
        if (match := get_match_by_id(current_user, tournament_id, match_id)) is not None
    ]

    return result


def update_match(
    current_user: UserModel, tournament_id: str, match_id: str, run_logs: str
) -> BotModel | None:
    match: MatchModel | None = get_match_by_id(current_user, tournament_id, match_id)
    if match is None:
        return None

    winner_code: str = run_logs.split(",")[0][1:]
    bot_1: BotModel | None = get_bot_by_id(match.players["bot1"])
    bot_2: BotModel | None = get_bot_by_id(match.players["bot2"])
    if bot_1 is None or bot_2 is None:
        return None

    winner_id, loser_id = (
        (bot_1.id, bot_2.id) if winner_code == bot_1.code else (bot_2.id, bot_1.id)
    )
    winner: BotModel | None = get_bot_by_id(winner_id)
    if winner is None:
        return None

    db = MongoDB()
    matches = Match(db)
    matches.set_winner(ObjectId(match_id), ObjectId(winner_id))
    bots = Bot(db)
    bots.update_stats(winner_id, won=True)
    bots.update_stats(loser_id, won=False)

    return winner
