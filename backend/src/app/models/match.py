from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from database.main import MongoDB, Bot, Match, Tournament
from app.schemas.match import MatchModel, MatchCreate
from app.schemas.tournament import TournamentModel
from app.models.bot import get_bot_by_id
from app.schemas.bot import BotModel
import app.utils.connection as conn


def get_match_by_id(db: MongoDB, match_id: ObjectId) -> dict[str, Any]:
    """
    Retrieves a match from the database by its ID.
    Raises an error if the match does not exist.
    """

    matches_collection = Match(db)
    match = matches_collection.get_match_by_id(match_id)

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return match


def convert_match(
    db: MongoDB, match_dict: dict[str, Any], detail: bool = False
) -> MatchModel:
    """
    Converts a dictionary to a MatchModel object.
    """

    players = match_dict.pop("players")
    match_dict["players"] = {}
    for key, bot_id in players.items():
        match_dict["players"][key] = get_bot_by_id(db, bot_id)

    winner_id = match_dict.pop("winner")
    if winner_id is not None:
        match_dict["winner"] = get_bot_by_id(db, winner_id)

    if not detail:
        match_dict.pop("moves")
        return MatchModel(**match_dict)

    return MatchModel(**match_dict)


def get_bots_by_match_id(db: MongoDB, match_id: ObjectId) -> dict[str, BotModel]:
    """
    Retrieves all bots from the database that participate in a specific match.
    """

    match_dict = get_match_by_id(db, match_id)
    match = convert_match(db, match_dict, detail=True)

    if match.players is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No bots not found for match: {match_id}.",
        )

    return match.players


def process_match(
    db: MongoDB, tournament: TournamentModel, match: MatchModel
) -> dict[str, BotModel]:
    """
    Runs the match on docker.
    Updates the database with the results of a match.
    Returns the winner and loser bots with updated stats.
    """

    bot_1, bot_2 = match.players.values()
    response = conn.run_match(tournament.game_type.name, bot_1.code, bot_2.code)
    i = 0

    while response["winner"] is None:
        response = conn.run_match(tournament.game_type.name, bot_1.code, bot_2.code)
        i += 1

        if i > 9:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Match: {match.id} ended in a draw.",
            )

    moves: list[str] = response["states"]
    if response["winner"] == 0:
        winner = bot_1
        loser = bot_2
    else:
        winner = bot_2
        loser = bot_1

    matches_collection = Match(db)
    matches_collection.set_winner(match.id, winner.id)
    for move in moves:
        matches_collection.add_move(match.id, move)

    bots_collection = Bot(db)
    bots_collection.update_stats(winner.id, won=True)
    bots_collection.update_stats(loser.id, won=False)

    return {
        "winner": get_bot_by_id(db, winner.id),
        "loser": get_bot_by_id(db, loser.id),
    }


def insert_match(
    db: MongoDB,
    tournament_id: ObjectId,
    match_data: MatchCreate,
) -> MatchModel:
    """
    Creates a new match in the database.
    Returns the created match.
    """

    matches_collection = Match(db)
    match_id = matches_collection.create_match(
        match_data.game_num, match_data.bot_1, match_data.bot_2
    )

    tournaments_collection = Tournament(db)
    tournaments_collection.add_match(tournament_id, match_id)

    match_dict = get_match_by_id(db, match_id)
    return convert_match(db, match_dict, detail=True)
