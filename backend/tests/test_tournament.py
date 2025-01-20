from fastapi import HTTPException
import pytest

from app.models.tournament import DBTournament
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


class TestTournamentModel:
    def test_init_data(self, db_connection, tournament_dict):
        db_tournament = DBTournament(db_connection, data=tournament_dict)

        assert db_tournament.id == tournament_dict["_id"]
        assert db_tournament.name == tournament_dict["name"]
        assert db_tournament.description == tournament_dict["description"]
        assert db_tournament.game_type == tournament_dict["game_type"]
        assert db_tournament.creator == tournament_dict["creator"]
        assert db_tournament.start_date == tournament_dict["start_date"]
        assert db_tournament.access_code == tournament_dict["access_code"]
        assert db_tournament.max_participants == tournament_dict["max_participants"]
        assert db_tournament.participants == tournament_dict["participants"]
        assert db_tournament.matches == tournament_dict["matches"]
        assert db_tournament.winner == tournament_dict["winner"]

    def test_init_id(self, db_connection, tournament_dict):
        with pytest.raises(HTTPException):
            _ = DBTournament(db_connection, id=tournament_dict["_id"])

    def test_to_schema(self, tournament_dict, insert_tournament):
        db_game_type, db_user, db_tournament = insert_tournament
        tournament_dict["game_type"] = db_game_type.to_schema()
        tournament_dict["creator"] = db_user.to_schema()
        tournament_dict["access_code"] = db_tournament.access_code
        tournament_dict["_id"] = db_tournament.id
        tournament = Tournament(**tournament_dict)

        assert db_tournament.to_schema() == tournament

    def test_insert(self, tournament_dict, insert_tournament):
        db_game_type, db_user, db_tournament = insert_tournament

        assert db_tournament.name == tournament_dict["name"]
        assert db_tournament.description == tournament_dict["description"]
        assert db_tournament.game_type == db_game_type.id
        assert db_tournament.creator == db_user.id
        assert db_tournament.start_date == tournament_dict["start_date"]
        assert len(db_tournament.access_code) == 6
        assert db_tournament.max_participants == tournament_dict["max_participants"]
        assert db_tournament.participants == []
        assert db_tournament.matches == []
        assert db_tournament.winner is None

    def test_get_all(self, db_connection, insert_tournament):
        db_tournament = insert_tournament[2]
        tournaments = DBTournament.get_all(db_connection)

        assert len(tournaments) == 1
        assert tournaments[0].id == db_tournament.id
