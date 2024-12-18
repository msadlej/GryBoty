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
    Retrieves a match from the database by its ID.
    Returns None if the match does not exist or the user does not have access to it.
    """

    db = MongoDB()
    matches = Match(db)
    match: dict[str, Any] | None = matches.get_match_by_id(ObjectId(match_id))
    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    return MatchModel(**match) if match is not None and tournament is not None else None


def get_matches_by_tournament(
    current_user: UserModel, tournament_id: str
) -> list[MatchModel] | None:
    """
    Retrieves all matches from the database that belong to a specific tournament.
    Returns None if the tournament does not exist or the user does not have access to it.
    """

    tournament: TournamentModel | None = get_tournament_by_id(
        current_user, tournament_id
    )

    return (
        [
            match
            for match_id in tournament.matches
            if (match := get_match_by_id(current_user, tournament_id, match_id))
            is not None
        ]
        if tournament is not None
        else None
    )


def get_bots_by_tournament(
    current_user: UserModel, tournament: TournamentModel
) -> list[BotModel] | None:
    """
    Retrieves all bots that are participating in a specific tournament.
    Returns None if the tournament does not exist or the user does not have access to it.
    """

    matches: list[MatchModel] | None = get_matches_by_tournament(
        current_user, tournament.id
    )
    if matches is None:
        return None

    return [
        bot
        for match in matches
        for bot_id in match.players.values()
        if (bot := get_bot_by_id(bot_id)) is not None
    ]


def update_match(
    current_user: UserModel,
    tournament_id: str,
    match_id: str,
    docker_logs: dict[str, Any],
) -> dict[str, BotModel] | None:
    """
    Runs a match and updates the database with the results.
    """

    match: MatchModel | None = get_match_by_id(current_user, tournament_id, match_id)
    if match is None:
        return None

    winner_code: str = docker_logs["winner"]
    moves: list[str] = docker_logs["moves"]

    bot_1: BotModel | None = get_bot_by_id(match.players["bot1"])
    bot_2: BotModel | None = get_bot_by_id(match.players["bot2"])
    if bot_1 is None or bot_2 is None:
        return None

    winner_id, loser_id = (
        (bot_1.id, bot_2.id) if winner_code == bot_1.code else (bot_2.id, bot_1.id)
    )

    db = MongoDB()
    matches = Match(db)
    matches.set_winner(ObjectId(match_id), ObjectId(winner_id))
    for move in moves:
        matches.add_move(ObjectId(match_id), move)

    bots = Bot(db)
    bots.update_stats(ObjectId(winner_id), won=True)
    bots.update_stats(ObjectId(loser_id), won=False)

    winner: BotModel | None = get_bot_by_id(winner_id)
    loser: BotModel | None = get_bot_by_id(loser_id)
    return (
        {"winner": winner, "loser": loser}
        if winner is not None and loser is not None
        else None
    )
