from app.models.match import convert_match
from app.schemas.match import MatchModel


def test_match_model(match_dict):
    match = MatchModel(**match_dict)

    assert match.id == match_dict["_id"]
    assert match.game_num == match_dict["game_num"]
    assert match.players == match_dict["players"]
    assert match.moves == match_dict["moves"]
    assert match.winner == match_dict["winner"]


def test_convert_match(match_dict):
    match: MatchModel = convert_match(match_dict, detail=False)

    assert match.players is None
    assert match.moves is None
    assert match.winner is None
