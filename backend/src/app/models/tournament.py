from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any
import random
import string

from app.schemas.tournament import TournamentModel, TournamentCreate, TournamentUpdate
from app.models.bot import get_bot_by_id, get_bots_by_user_id
from app.models.match import get_match_by_id, convert_match
from app.models.user import get_user_by_id, convert_user
from app.schemas.user import AccountType, UserModel
from app.models.game import get_game_type_by_id
from database.main import MongoDB, Tournament
from app.schemas.match import MatchModel
from app.schemas.bot import BotModel


def generate_access_code(length: int = 6) -> str:
    """
    Generates a random access code with digits and capital letters.
    """

    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def check_tournament_creator(
    db: MongoDB, current_user: UserModel, tournament_id: ObjectId
) -> bool:
    """
    Checks if the user is the creator of the tournament or an admin.
    """

    tournament = get_tournament_by_id(db, tournament_id)

    is_admin: bool = current_user.account_type is AccountType.ADMIN
    is_creator: bool = current_user.id == tournament["creator"]

    return is_creator or is_admin


def check_tournament_access(
    db: MongoDB, current_user: UserModel, tournament_id: ObjectId
) -> bool:
    """
    Checks if the user has access to the tournament.
    """

    tournament = get_tournament_by_id(db, tournament_id)

    if current_user.bots is None:
        current_user.bots = get_bots_by_user_id(db, current_user.id)

    is_admin: bool = current_user.account_type is AccountType.ADMIN
    is_creator: bool = current_user.id == tournament["creator"]
    is_participant: bool = any(
        bot.id in tournament["participants"] for bot in current_user.bots
    )

    return any((is_admin, is_creator, is_participant))


def get_tournament_by_id(db, tournament_id: ObjectId) -> dict[str, Any]:
    """
    Retrieves a tournament from the database by its ID.
    Raises an error if the tournament does not exist.
    """

    tournaments_collection = Tournament(db)
    tournament = tournaments_collection.get_tournament_by_id(tournament_id)

    if tournament is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return tournament


def get_tournament_id_by_access_code(db: MongoDB, access_code: str) -> ObjectId | None:
    """
    Retrieves a tournament ID from the database by its access code.
    Returns None if the access code does not exist.
    """

    tournaments_collection = Tournament(db)
    tournament = tournaments_collection.get_tournament_by_access_code(access_code)

    return tournament["_id"] if tournament else None


def convert_tournament(
    db: MongoDB, tournament_dict: dict[str, Any], detail: bool = False
) -> TournamentModel:
    """
    Converts a tournament dictionary to a TournamentModel.
    """

    game_type = tournament_dict.pop("game_type")
    tournament_dict["game_type"] = get_game_type_by_id(db, game_type)

    creator = tournament_dict.pop("creator")
    user_dict = get_user_by_id(db, creator)
    tournament_dict["creator"] = convert_user(db, user_dict)

    participant_ids = tournament_dict.pop("participants")
    match_ids = tournament_dict.pop("matches")
    if not detail:
        return TournamentModel(**tournament_dict)

    participants = []
    for bot_id in participant_ids:
        bot = get_bot_by_id(db, bot_id)
        participants.append(bot)

    matches = []
    for match_id in match_ids:
        match_dict = get_match_by_id(db, match_id)
        matches.append(convert_match(db, match_dict))

    tournament_dict["participants"] = participants
    tournament_dict["matches"] = matches

    return TournamentModel(**tournament_dict)


def get_bots_by_tournament(db: MongoDB, tournament_id: ObjectId) -> list[BotModel]:
    """
    Retrieves all bots from the database that participate in a specific tournament.
    """

    tournament = get_tournament_by_id(db, tournament_id)

    return [get_bot_by_id(db, bot_id) for bot_id in tournament["participants"]]


def get_matches_by_tournament(db: MongoDB, tournament_id: ObjectId) -> list[MatchModel]:
    """
    Retrieves all matches from the database that belong to a specific tournament.
    """

    tournament = get_tournament_by_id(db, tournament_id)

    return [
        convert_match(db, match_dict)
        for match_id in tournament["matches"]
        if (match_dict := get_match_by_id(db, match_id))
    ]


def get_tournaments_by_user_id(db: MongoDB, user_id: ObjectId) -> list[TournamentModel]:
    """
    Retrieves all tournaments that the user has created or is participating in.
    """

    tournaments_collection = Tournament(db)
    tournaments = tournaments_collection.get_tournaments_by_creator(user_id)

    bots = get_bots_by_user_id(db, user_id)
    for bot in bots:
        tournaments.extend(tournaments_collection.get_tournaments_by_bot_id(bot.id))

    return [convert_tournament(db, tournament) for tournament in tournaments]


def get_all_tournaments(db: MongoDB) -> list[TournamentModel]:
    """
    Retrieves all tournaments from the database.
    """

    tournaments_collection = Tournament(db)
    tournaments = tournaments_collection.get_all_tournaments()

    return [convert_tournament(db, tournament) for tournament in tournaments]


def insert_tournament(
    db: MongoDB, current_premium_user: UserModel, tournament: TournamentCreate
) -> TournamentModel:
    """
    Inserts a new tournament into the database.
    Returns the created tournament.
    """

    if get_game_type_by_id(db, tournament.game_type) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game type: {tournament.game_type} not found.",
        )

    access_code = generate_access_code()
    i = 0
    while get_tournament_id_by_access_code(db, access_code) is not None:
        if i > 9:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate unique access code.",
            )

        access_code = generate_access_code()
        i += 1

    tournaments_collection = Tournament(db)
    tournament_id = tournaments_collection.create_tournament(
        tournament.name,
        tournament.description,
        tournament.game_type,
        current_premium_user.id,
        tournament.start_date,
        access_code,
        tournament.max_participants,
    )

    tournament_dict = get_tournament_by_id(db, tournament_id)
    return convert_tournament(db, tournament_dict, detail=True)


def update_tournament(
    db: MongoDB, tournament_id: ObjectId, tournament_data: TournamentUpdate
) -> TournamentModel:
    """
    Updates an existing tournament in the database.
    Returns the updated tournament.
    """

    tournaments_collection = Tournament(db)
    tournament_dict = get_tournament_by_id(db, tournament_id)
    tournament = convert_tournament(db, tournament_dict)
    # TODO: Check if the tournament is finished.
    # if tournament.winner is not None:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"Tournament: {tournament_id} is already finished.",
    #     )

    if tournament_data.name is not None:
        tournaments_collection.update_name(tournament_id, tournament_data.name)

    if tournament_data.description is not None:
        tournaments_collection.update_description(
            tournament_id, tournament_data.description
        )

    if tournament_data.start_date is not None:
        tournaments_collection.update_start_date(
            tournament_id, tournament_data.start_date
        )

    if tournament_data.max_participants is not None:
        tournaments_collection.update_max_participants(
            tournament_id, tournament_data.max_participants
        )

    # if tournament_data.winner_id is not None:
    #     tournaments_collection.update_winner(tournament_id, tournament_data.winner_id)

    tournament_dict = get_tournament_by_id(db, tournament_id)
    return convert_tournament(db, tournament_dict, detail=True)


def add_tournament_participant(
    db: MongoDB, tournament_id: ObjectId, bot_id: ObjectId
) -> TournamentModel:
    """
    Adds a bot to a tournament.
    Returns the updated tournament.
    """

    tournament_dict = get_tournament_by_id(db, tournament_id)
    tournament = convert_tournament(db, tournament_dict, detail=True)
    bot = get_bot_by_id(db, bot_id)
    if bot.game_type != tournament.game_type:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bot: {bot_id} does not match the game type of the tournament.",
        )
    if not bot.is_validated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bot: {bot_id} is not validated.",
        )

    # TODO: Check if the creator of the bot already has a bot in the tournament.
    # if any(bot.creator == participant.creator for participant in tournament.participants):
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"User: {bot.creator} already has a bot in the tournament"
    #     )
    # TODO: Check if the tournament is finished.
    # if tournament.winner is not None:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=f"Tournament: {tournament_id} is already finished.",
    #     )

    tournaments_collection = Tournament(db)
    success = tournaments_collection.add_participant(tournament_id, bot_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tournament: {tournament_id} is already full.",
        )

    tournament_dict = get_tournament_by_id(db, tournament_id)
    return convert_tournament(db, tournament_dict, detail=True)
