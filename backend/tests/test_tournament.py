from app.schemas.tournament import TournamentModel
from app.models.tournament import convert_tournament
from bson import ObjectId


def test_tournament_model(tournament_dict):
    tournament = TournamentModel(**tournament_dict)

    assert ObjectId(tournament.id) == tournament_dict["_id"]
    assert tournament.name == tournament_dict["name"]
    assert tournament.description == tournament_dict["description"]
    assert tournament.game_type == tournament_dict["game_type"]
    assert tournament.creator == tournament_dict["creator"]
    assert tournament.start_date == tournament_dict["start_date"]
    assert tournament.access_code == tournament_dict["access_code"]
    assert tournament.max_participants == tournament_dict["max_participants"]
    assert tournament.participants == tournament_dict["participants"]
    assert tournament.matches == tournament_dict["matches"]


def test_convert_tournament(tournament_dict):
    tournament: TournamentModel = convert_tournament(tournament_dict, detail=False)

    assert ObjectId(tournament.id) == tournament_dict["_id"]
    assert tournament.name == tournament_dict["name"]
    assert tournament.description == tournament_dict["description"]
    assert tournament.game_type is None
    assert tournament.creator is None
    assert tournament.start_date == tournament_dict["start_date"]
    assert tournament.access_code == tournament_dict["access_code"]
    assert tournament.max_participants == tournament_dict["max_participants"]
    assert tournament.participants is None
    assert tournament.matches is None
