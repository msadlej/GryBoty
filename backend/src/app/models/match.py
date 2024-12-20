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


def convert_match(match_dict: dict[str, Any]) -> MatchModel:
    """
    Converts a dictionary to a MatchModel object.
    """

    for key, value in match_dict["players"].items():
        if value is not None:
            bot: dict[str, Any] | None = get_bot_by_id(value)
            bot.pop("game_type")
            match_dict["players"][key] = bot

    if match_dict["winner"] is not None:
        winner: dict[str, Any] | None = get_bot_by_id(match_dict["winner"])
        winner.pop("game_type")
        match_dict["winner"] = winner

    return MatchModel(**match_dict)


def get_bots_by_match(match_id: str) -> dict[str, BotModel | None] | None:
    """
    Retrieves all bots from the database that participate in a specific match.
    Returns None if the match does not exist.
    """

    match: dict[str, Any] | None = get_match_by_id(match_id)
    if match is None:
        return None

    result: dict[str, BotModel] = {}
    for key, value in match["players"].items():
        if value is not None:
            bot: dict[str, Any] | None = get_bot_by_id(value)

            if bot is None:
                result[key] = None
            else:
                bot.pop("game_type")
                result[key] = BotModel(**bot)

    return result


def update_match(
    match: MatchModel,
    docker_logs: dict[str, Any],
) -> dict[str, BotModel] | None:
    """
    Runs a match and updates the database with the results.
    """

    moves: list[str] = docker_logs["moves"]
    winner_code: str = docker_logs["winner"]
    if winner_code == None:
        return None  # TODO: Update stats after a draw

    bot_1: dict[str, Any] | None = get_bot_by_id(match.players["bot1"].id)
    bot_2: dict[str, Any] | None = get_bot_by_id(match.players["bot2"].id)
    if bot_1 is None or bot_2 is None:
        return None

    winner, loser = (bot_1, bot_2) if winner_code == bot_1["code"] else (bot_2, bot_1)
    winner: BotModel = convert_bot(winner)
    loser: BotModel = convert_bot(loser)

    db = MongoDB()
    matches_collection = Match(db)
    matches_collection.set_winner(ObjectId(match.id), ObjectId(winner.id))
    for move in moves:
        matches_collection.add_move(ObjectId(match.id), move)

    bots_collection = Bot(db)
    bots_collection.update_stats(ObjectId(winner.id), won=True)
    bots_collection.update_stats(ObjectId(loser.id), won=False)

    return get_bots_by_match(match.id)
