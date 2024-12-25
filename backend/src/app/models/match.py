from app.models.bot import get_bot_by_id, convert_bot
from database.main import MongoDB, Bot, Match
from fastapi import HTTPException, status
from app.schemas.match import MatchModel
from app.schemas.bot import BotModel
from bson import ObjectId
from typing import Any


def get_match_by_id(match_id: str) -> dict[str, Any]:
    """
    Retrieves a match from the database by its ID.
    Raises an error if the match does not exist.
    """

    db = MongoDB()
    matches_collection = Match(db)
    match: dict[str, Any] | None = matches_collection.get_match_by_id(
        ObjectId(match_id)
    )

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return match


def convert_match(match_dict: dict[str, Any], detail: bool = False) -> MatchModel:
    """
    Converts a dictionary to a MatchModel object.
    """

    players: dict[str, str] = match_dict.pop("players")
    winner_id: str | None = match_dict.pop("winner")
    if not detail:
        match_dict.pop("moves")
        return MatchModel(**match_dict)

    match_dict["players"] = {}
    for key, bot_id in players.items():
        bot: dict[str, Any] = get_bot_by_id(bot_id)
        match_dict["players"][key] = convert_bot(bot)

    if winner_id is not None:
        winner: dict[str, Any] = get_bot_by_id(winner_id)
        match_dict["winner"] = convert_bot(winner)

    return MatchModel(**match_dict)


def get_bots_by_match(match_id: str) -> dict[str, BotModel]:
    """
    Retrieves all bots from the database that participate in a specific match.
    """

    match: MatchModel = convert_match(get_match_by_id(match_id), detail=True)

    if match.players is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No bots not found for match: {match_id}.",
        )

    return match.players


def update_match(
    match: MatchModel,
    winner: BotModel,
    loser: BotModel,
    moves: list[str],
) -> dict[str, BotModel]:
    """
    Updates the database with the results of a match.
    Returns the winner and loser bots with updated stats.
    Returns None if the bots do not exist.
    """

    db = MongoDB()
    matches_collection = Match(db)
    matches_collection.set_winner(ObjectId(match.id), ObjectId(winner.id))
    for move in moves:
        matches_collection.add_move(ObjectId(match.id), move)

    bots_collection = Bot(db)
    bots_collection.update_stats(ObjectId(winner.id), won=True)
    bots_collection.update_stats(ObjectId(loser.id), won=False)

    winner_dict = get_bot_by_id(winner.id)
    loser_dict = get_bot_by_id(loser.id)

    return {
        "winner": convert_bot(winner_dict),
        "loser": convert_bot(loser_dict),
    }


def process_logs(
    match: MatchModel,
    docker_logs: dict[str, Any],
    bot_1: dict[str, Any],
    bot_2: dict[str, Any],
) -> tuple[list[str], BotModel, BotModel] | tuple[list[str], None, None]:
    """
    Processes the logs from a match and returns the moves, the winner and loser bots.
    Returns None if the match ended in a draw.
    """

    moves: list[str] = docker_logs["moves"]
    winner_code: str | None = docker_logs["winner"]
    if winner_code is None:
        return moves, None, None

    if match.players is None:
        match.players = get_bots_by_match(match.id)

    if winner_code == bot_1["code"]:
        winner: BotModel = convert_bot(bot_1)
        loser: BotModel = convert_bot(bot_2)
    elif winner_code == bot_2["code"]:
        winner = convert_bot(bot_2)
        loser = convert_bot(bot_1)
    else:
        return moves, None, None

    return moves, winner, loser
