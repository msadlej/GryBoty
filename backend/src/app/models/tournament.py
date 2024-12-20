from app.models.bot import get_bot_by_id, convert_bot, get_own_bots
from app.models.match import get_match_by_id, convert_match
from app.models.user import get_user_by_id, convert_user
from app.schemas.user import AccountType, UserModel
from app.schemas.tournament import TournamentModel
from app.models.game import get_game_type_by_id
from database.main import MongoDB, Tournament
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


def convert_tournament(
    tournament_dict: dict[str, Any], detail: bool = False
) -> TournamentModel:
    """
    Converts a tournament dictionary to a TournamentModel.
    """

    game_type: str = tournament_dict.pop("game_type")
    creator: str = tournament_dict.pop("creator")
    participant_ids: list[str] = tournament_dict.pop("participants")
    match_ids: list[str] = tournament_dict.pop("matches")
    if not detail:
        return TournamentModel(**tournament_dict)

    tournament_dict["game_type"] = get_game_type_by_id(game_type)

    user: dict[str, Any] | None = get_user_by_id(creator)
    if user is not None:
        tournament_dict["creator"] = convert_user(user)

    participants: list[BotModel] = []
    for bot_id in participant_ids:
        bot: dict[str, Any] | None = get_bot_by_id(bot_id)

        if bot is not None:
            participants.append(convert_bot(bot))
    tournament_dict["participants"] = participants

    matches: list[MatchModel] = []
    for match_id in match_ids:
        match: dict[str, Any] | None = get_match_by_id(match_id)

        if match is not None:
            matches.append(convert_match(match))
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

    bots: list[dict[str, Any]] = [
        bot
        for bot_id in tournament["participants"]
        if (bot := get_bot_by_id(bot_id)) is not None
    ]

    return [convert_bot(bot) for bot in bots]


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

    return [convert_match(match) for match in matches]


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

    return [convert_tournament(tournament) for tournament in tournaments]


def get_all_tournaments() -> list[TournamentModel]:
    """
    Retrieves all tournaments from the database.
    """

    db = MongoDB()
    tournaments_collection = Tournament(db)
    tournaments: list[dict[str, Any]] = tournaments_collection.get_all_tournaments()

    return [convert_tournament(tournament) for tournament in tournaments]
