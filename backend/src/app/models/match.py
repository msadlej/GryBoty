from app.models.bot import get_bot_by_id, convert_bot
from database.main import MongoDB, Bot, Match
from app.schemas.match import MatchModel
from app.schemas.bot import BotModel
from bson import ObjectId
from typing import Any


def get_match_by_id(match_id: str) -> dict[str, Any] | None:
    """
    Retrieves a match from the database by its ID.
    Returns None if the match does not exist.
    """

    db = MongoDB()
    matches_collection = Match(db)
    match: dict[str, Any] | None = matches_collection.get_match_by_id(
        ObjectId(match_id)
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
        bot: dict[str, Any] | None = get_bot_by_id(bot_id)

        if bot is not None:
            match_dict["players"][key] = convert_bot(bot)

    if winner_id is not None:
        winner: dict[str, Any] | None = get_bot_by_id(winner_id)

        if winner is not None:
            match_dict["winner"] = convert_bot(winner)

    return MatchModel(**match_dict)


def get_bots_by_match(match_id: str) -> dict[str, BotModel] | None:
    """
    Retrieves all bots from the database that participate in a specific match.
    Returns None if the match does not exist.
    """

    match_dict: dict[str, Any] | None = get_match_by_id(match_id)
    if match_dict is None:
        return None

    match: MatchModel = convert_match(match_dict, detail=True)
    return match.players


def update_match(
    match: MatchModel,
    docker_logs: dict[str, Any],
) -> dict[str, BotModel] | None:
    """
    Runs a match and updates the database with the results.
    """

    moves: list[str] = docker_logs["moves"]
    winner_code: str | None = docker_logs["winner"]
    if winner_code is None:
        return None  # TODO: Update stats after a draw

    if match.players is None:
        return None

    bot_1: dict[str, Any] | None = get_bot_by_id(match.players["bot1"].id)
    bot_2: dict[str, Any] | None = get_bot_by_id(match.players["bot2"].id)
    if bot_1 is None or bot_2 is None:
        return None

    if winner_code == bot_1["code"]:
        winner: BotModel = convert_bot(bot_1)
        loser: BotModel = convert_bot(bot_2)
    elif winner_code == bot_2["code"]:
        winner = convert_bot(bot_2)
        loser = convert_bot(bot_1)
    else:
        return None

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
    if winner_dict is None or loser_dict is None:
        return None

    return {
        "winner": convert_bot(winner_dict),
        "loser": convert_bot(loser_dict),
    }
