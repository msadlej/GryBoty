from contextlib import contextmanager
from datetime import datetime
from bson import ObjectId
import mongomock
import pytest

from app.utils.authentication import get_password_hash
from app.schemas.match import MatchModel
from app.schemas.game import GameModel
from app.schemas.user import UserModel
from app.schemas.bot import BotModel
from database.main import MongoDB


@pytest.fixture
def game_dict():
    return {
        "_id": ObjectId(),
        "name": "Test Game",
        "description": "Test Description",
    }


@pytest.fixture
def bot_dict(game_dict):
    return {
        "_id": ObjectId(),
        "name": "Test Bot",
        "game_type": GameModel(**game_dict),
        "code_path": "path/to/bot.py",
        "is_validated": True,
        "games_played": 4,
        "wins": 3,
        "losses": 2,
        "total_tournaments": 1,
        "tournaments_won": 0,
    }


@pytest.fixture
def user_dict(bot_dict):
    return {
        "_id": ObjectId(),
        "username": "username",
        "account_type": "standard",
        "bots": [BotModel(**bot_dict)],
        "is_banned": True,
    }


@pytest.fixture
def match_dict(bot_dict):
    return {
        "_id": ObjectId(),
        "game_num": 1,
        "players": {"player1": BotModel(**bot_dict), "player2": BotModel(**bot_dict)},
        "moves": ["move1", "move2"],
        "winner": BotModel(**bot_dict),
    }


@pytest.fixture
def tournament_dict(game_dict, bot_dict, user_dict, match_dict):
    return {
        "_id": ObjectId(),
        "name": "Test Tournament",
        "description": "Test Description",
        "game_type": GameModel(**game_dict),
        "creator": UserModel(**user_dict),
        "start_date": datetime(2024, 12, 24),
        "access_code": "12345",
        "max_participants": 4,
        "participants": [BotModel(**bot_dict)],
        "matches": [MatchModel(**match_dict)],
    }


@pytest.fixture
def patch_get_user_by_username(monkeypatch):
    def mock_get(_, username: str | None) -> UserModel | None:
        return (
            {
                "_id": ObjectId(),
                "username": "username",
                "password_hash": get_password_hash("password"),
                "account_type": "standard",
                "bots": [],
                "is_banned": False,
            }
            if username == "username"
            else None
        )

    monkeypatch.setattr("app.utils.authentication.get_user_by_username", mock_get)
    monkeypatch.setattr("app.dependencies.get_user_by_username", mock_get)


@contextmanager
def mock_get_db_connection(connection_string: str = "mongodb://localhost:27017/"):
    client = mongomock.MongoClient()
    db = MongoDB()
    db.client = client
    db.db = client.pzsp_database
    try:
        yield db
    finally:
        client.close()


@pytest.fixture
def db_connection():
    with mock_get_db_connection() as db:
        yield db
