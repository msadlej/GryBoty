from app.models.bot import get_bot_by_id, get_own_bots
from app.schemas.user import AccountType, UserModel
from app.schemas.tournament import TournamentModel
from app.models.game import get_game_type_by_id
from database.main import MongoDB, Tournament
from app.models.match import get_match_by_id
from app.models.user import get_user_by_id
from app.schemas.match import MatchModel
from app.schemas.bot import BotModel
from bson import ObjectId
from typing import Any


def check_tournament_creator(current_user: UserModel, tournament_id: str) -> bool:
    """
    Checks if the user is the creator of the tournament or an admin.
    """

    tournament: dict[str, Any] | None = get_tournament_by_id(tournament_id)
    if tournament is None:
        return False

    is_admin: bool = current_user.account_type == AccountType.ADMIN
    is_creator: bool = ObjectId(current_user.id) == tournament["creator"]

    return is_creator or is_admin


def check_tournament_access(current_user: UserModel, tournament_id: str) -> bool:
    """
    Checks if the user has access to the tournament.
    """

    tournament: dict[str, Any] | None = get_tournament_by_id(tournament_id)
    if tournament is None:
        return False

    if current_user.bots is None:
        current_user.bots = get_own_bots(current_user)

    is_admin: bool = current_user.account_type == AccountType.ADMIN
    is_creator: bool = ObjectId(current_user.id) == tournament["creator"]
    is_participant: bool = any(
        ObjectId(bot.id) in tournament["participants"] for bot in current_user.bots
    )

    return any((is_admin, is_creator, is_participant))


def get_tournament_by_id(tournament_id: str) -> dict[str, Any] | None:
    """
    Retrieves a tournament from the database by its ID.
    Returns None if the tournament does not exist.
    """

    db = MongoDB()
    tournaments_collection = Tournament(db)
    return tournaments_collection.get_tournament_by_id(ObjectId(tournament_id))


def convert_tournament(tournament_dict: dict[str, Any]) -> TournamentModel:
    """
    Converts a tournament dictionary to a TournamentModel.
    """

    tournament_dict["game_type"] = get_game_type_by_id(tournament_dict["game_type"])

    user: dict[str, Any] = get_user_by_id(tournament_dict["creator"])
    user.pop("bots")
    tournament_dict["creator"] = user

    participants: list[dict[str, Any]] = []
    for bot_id in tournament_dict["participants"]:
        bot: dict[str, Any] | None = get_bot_by_id(bot_id)
        bot.pop("game_type")
        participants.append(bot)
    tournament_dict["participants"] = participants

    matches: list[dict[str, Any]] = []
    for match_id in tournament_dict["matches"]:
        match: dict[str, Any] | None = get_match_by_id(match_id)
        match.pop("players")
        match.pop("moves")
        match.pop("winner")
        matches.append(match)
    tournament_dict["matches"] = matches

    return TournamentModel(**tournament_dict)


def get_bots_by_tournament(tournament_id: str) -> list[BotModel] | None:
    """
    Retrieves all bots from the database that participate in a specific tournament.
    Returns None if the tournament does not exist.
    """

    tournament: dict[str, Any] | None = get_tournament_by_id(tournament_id)
    if tournament is None:
        return None

    result: list[BotModel] = []
    for bot_id in tournament["participants"]:
        bot: dict[str, Any] | None = get_bot_by_id(bot_id)
        if bot is not None:
            bot.pop("game_type")
            result.append(BotModel(**bot))

    return result


def get_matches_by_tournament(tournament_id: str) -> list[MatchModel] | None:
    """
    Retrieves all matches from the database that belong to a specific tournament.
    Returns None if the tournament does not exist.
    """

    tournament: dict[str, Any] | None = get_tournament_by_id(tournament_id)
    if tournament is None:
        return None

    matches: list[dict[str, Any]] = [
        match
        for match_id in tournament["matches"]
        if (match := get_match_by_id(match_id)) is not None
    ]

    for match in matches:
        match.pop("players")
        match.pop("moves")
        match.pop("winner")

    return [MatchModel(**match) for match in matches]


def get_own_tournaments(current_user: UserModel) -> list[TournamentModel]:
    """
    Retrieves all tournaments that the user has created or is participating in.
    """

    db = MongoDB()
    tournaments_collection = Tournament(db)
    tournaments: list[dict[str, Any]] = (
        tournaments_collection.get_tournaments_by_creator(ObjectId(current_user.id))
    )

    if current_user.bots is None:
        current_user.bots = get_own_bots(current_user)
    for bot in current_user.bots:
        tournaments.extend(
            tournaments_collection.get_tournaments_by_bot_id(ObjectId(bot.id))
        )

    result: list[TournamentModel] = []
    for tournament in tournaments:
        tournament.pop("game_type")
        tournament.pop("creator")
        tournament.pop("participants")
        tournament.pop("matches")
        result.append(TournamentModel(**tournament))

    return result


def get_all_tournaments() -> list[TournamentModel]:
    """
    Retrieves all tournaments from the database.
    """

    db = MongoDB()
    tournaments_collection = Tournament(db)
    tournaments: list[dict[str, Any]] = tournaments_collection.get_all_tournaments()

    result: list[TournamentModel] = []
    for tournament in tournaments:
        tournament.pop("game_type")
        tournament.pop("creator")
        tournament.pop("participants")
        tournament.pop("matches")
        result.append(TournamentModel(**tournament))

    return result
