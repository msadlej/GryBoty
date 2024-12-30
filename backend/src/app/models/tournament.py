from app.models.bot import get_bot_by_id, convert_bot, get_own_bots, get_bots_by_user_id
from app.models.match import get_match_by_id, convert_match
from app.models.user import get_user_by_id, convert_user
from app.schemas.user import AccountType, UserModel
from app.schemas.tournament import TournamentModel
from app.utils.database import get_db_connection
from app.models.game import get_game_type_by_id
from fastapi import HTTPException, status
from app.schemas.match import MatchModel
from app.schemas.bot import BotModel
from database.main import Tournament
from bson import ObjectId
from typing import Any


def check_tournament_creator(current_user: UserModel, tournament_id: str) -> bool:
    """
    Checks if the user is the creator of the tournament or an admin.
    """

    tournament = get_tournament_by_id(tournament_id)

    is_admin: bool = current_user.account_type is AccountType.ADMIN
    is_creator: bool = ObjectId(current_user.id) == tournament["creator"]

    return is_creator or is_admin


def check_tournament_access(current_user: UserModel, tournament_id: str) -> bool:
    """
    Checks if the user has access to the tournament.
    """

    tournament = get_tournament_by_id(tournament_id)

    if current_user.bots is None:
        current_user.bots = get_own_bots(current_user)

    is_admin: bool = current_user.account_type is AccountType.ADMIN
    is_creator: bool = ObjectId(current_user.id) == tournament["creator"]
    is_participant: bool = any(
        ObjectId(bot.id) in tournament["participants"] for bot in current_user.bots
    )

    return any((is_admin, is_creator, is_participant))


def get_tournament_by_id(tournament_id: str) -> dict[str, Any]:
    """
    Retrieves a tournament from the database by its ID.
    Raises an error if the tournament does not exist.
    """

    with get_db_connection() as db:
        tournaments_collection = Tournament(db)
        tournament: dict[str, Any] | None = tournaments_collection.get_tournament_by_id(
            ObjectId(tournament_id)
        )

    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return tournament


def convert_tournament(
    tournament_dict: dict[str, Any], detail: bool = False
) -> TournamentModel:
    """
    Converts a tournament dictionary to a TournamentModel.
    """

    game_type = tournament_dict.pop("game_type")
    creator = tournament_dict.pop("creator")
    participant_ids = tournament_dict.pop("participants")
    match_ids = tournament_dict.pop("matches")
    if not detail:
        return TournamentModel(**tournament_dict)

    user_dict = get_user_by_id(creator)

    participants = []
    for bot_id in participant_ids:
        bot_dict = get_bot_by_id(bot_id)
        participants.append(convert_bot(bot_dict))

    matches = []
    for match_id in match_ids:
        match_dict = get_match_by_id(match_id)
        matches.append(convert_match(match_dict))

    tournament_dict["game_type"] = get_game_type_by_id(game_type)
    tournament_dict["creator"] = convert_user(user_dict)
    tournament_dict["participants"] = participants
    tournament_dict["matches"] = matches

    return TournamentModel(**tournament_dict)


def get_bots_by_tournament(tournament_id: str) -> list[BotModel]:
    """
    Retrieves all bots from the database that participate in a specific tournament.
    """

    tournament = get_tournament_by_id(tournament_id)

    return [
        convert_bot(bot_dict)
        for bot_id in tournament["participants"]
        if (bot_dict := get_bot_by_id(bot_id))
    ]


def get_matches_by_tournament(tournament_id: str) -> list[MatchModel]:
    """
    Retrieves all matches from the database that belong to a specific tournament.
    """

    tournament = get_tournament_by_id(tournament_id)

    return [
        convert_match(match_dict)
        for match_id in tournament["matches"]
        if (match_dict := get_match_by_id(match_id))
    ]


def get_tournaments_by_user_id(user_id: str) -> list[TournamentModel]:
    """
    Retrieves all tournaments from the database that belong to a specific user.
    """

    with get_db_connection() as db:
        tournaments_collection = Tournament(db)
        tournaments = tournaments_collection.get_tournaments_by_creator(
            ObjectId(user_id)
        )

        bots = get_bots_by_user_id(user_id)
        for bot in bots:
            tournaments.extend(
                tournaments_collection.get_tournaments_by_bot_id(ObjectId(bot.id))
            )

    return [convert_tournament(tournament) for tournament in tournaments]


def get_own_tournaments(current_user: UserModel) -> list[TournamentModel]:
    """
    Retrieves all tournaments that the user has created or is participating in.
    """

    return get_tournaments_by_user_id(current_user.id)


def get_all_tournaments() -> list[TournamentModel]:
    """
    Retrieves all tournaments from the database.
    """

    with get_db_connection() as db:
        tournaments_collection = Tournament(db)
        tournaments = tournaments_collection.get_all_tournaments()

    return [convert_tournament(tournament) for tournament in tournaments]
