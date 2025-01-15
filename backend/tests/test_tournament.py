from datetime import datetime
import pytest

from app.models.tournament import convert_tournament, insert_tournament
from app.schemas.tournament import TournamentModel, TournamentCreate
from app.schemas.user import AccountType, UserUpdate
from app.models.user import insert_user, update_user
from app.models.game import insert_game_type
from app.schemas.game import GameCreate


def test_tournament_model(tournament_dict):
    tournament = TournamentModel(**tournament_dict)

    assert tournament.id == tournament_dict["_id"]
    assert tournament.name == tournament_dict["name"]
    assert tournament.description == tournament_dict["description"]
    assert tournament.game_type == tournament_dict["game_type"]
    assert tournament.creator == tournament_dict["creator"]
    assert tournament.start_date == tournament_dict["start_date"]
    assert tournament.access_code == tournament_dict["access_code"]
    assert tournament.max_participants == tournament_dict["max_participants"]
    assert tournament.participants == tournament_dict["participants"]
    assert tournament.matches == tournament_dict["matches"]


@pytest.mark.skip(reason="No longer needed")
def test_convert_tournament(tournament_dict):
    tournament: TournamentModel = convert_tournament(..., tournament_dict, detail=False)

    assert tournament.game_type is None
    assert tournament.creator is None
    assert tournament.participants is None
    assert tournament.matches is None


def test_insert_tournament(db_connection):
    user = insert_user(db_connection, "username", "password")
    user_data = UserUpdate(account_type=AccountType.PREMIUM)
    user = update_user(db_connection, user["_id"], user_data)

    game_create = GameCreate(name="Chess", description="A strategic board game")
    game = insert_game_type(db_connection, game_create)

    tournament_data = TournamentCreate(
        name="Tournament",
        description="A Chess Tournament",
        game_type=game.id,
        start_date=datetime.now(),
        max_participants=8,
    )

    tournament = insert_tournament(db_connection, user, tournament_data)

    assert isinstance(tournament, TournamentModel)
    assert tournament.name == "Tournament"
    assert tournament.description == "A Chess Tournament"
    assert tournament.game_type == game
    assert tournament.creator == user
    assert tournament.start_date is not None
    assert tournament.access_code is not None
    assert tournament.max_participants == 8
    assert tournament.participants == []
    assert tournament.matches == []
