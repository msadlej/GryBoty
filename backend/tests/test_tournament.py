from app.schemas.tournament import Tournament


def test_tournament_schema(tournament_dict):
    tournament = Tournament(**tournament_dict)

    assert tournament.id == tournament_dict["_id"]
    assert tournament.name == tournament_dict["name"]
    assert tournament.description == tournament_dict["description"]
    assert tournament.game_type == tournament_dict["game_type"]
    assert tournament.creator == tournament_dict["creator"]
    assert tournament.start_date == tournament_dict["start_date"]
    assert tournament.access_code == tournament_dict["access_code"]
    assert tournament.max_participants == tournament_dict["max_participants"]
