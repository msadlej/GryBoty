from app.schemas.match import Match


def test_match_schema(match_dict):
    match = Match(**match_dict)

    assert match.id == match_dict["_id"]
    assert match.game_num == match_dict["game_num"]
    assert match.players == match_dict["players"]
    assert match.moves == match_dict["moves"]
    assert match.winner == match_dict["winner"]
