from contextlib import contextmanager
from datetime import datetime
from bson import ObjectId
from typing import Any
import mongomock
import pytest

from app.utils.authentication import get_password_hash
from app.schemas.game_type import GameType
from database.main import MongoDB
from app.schemas.user import User
from app.schemas.bot import Bot


@pytest.fixture
def game_type_dict():
    return {
        "_id": ObjectId(),
        "name": "Test Game",
        "description": "Test Description",
    }


@pytest.fixture
def user_dict():
    return {
        "_id": ObjectId(),
        "username": "username",
        "password_hash": "password_hash",
        "account_type": "standard",
        "bots": [],
        "is_banned": False,
    }


@pytest.fixture
def bot_dict(game_type_dict):
    return {
        "_id": ObjectId(),
        "name": "Test Bot",
        "game_type": GameType(**game_type_dict),
        "code": b"print('Hello, World!')",
        "is_validated": True,
        "games_played": 4,
        "wins": 3,
        "losses": 2,
        "total_tournaments": 1,
        "tournaments_won": 0,
    }


@pytest.fixture
def match_dict(bot_dict):
    return {
        "_id": ObjectId(),
        "game_num": 1,
        "players": (Bot(**bot_dict), Bot(**bot_dict)),
        "moves": ["move1", "move2"],
        "winner": Bot(**bot_dict),
    }


@pytest.fixture
def tournament_dict(game_type_dict, bot_dict, user_dict, match_dict):
    return {
        "_id": ObjectId(),
        "name": "Test Tournament",
        "description": "Test Description",
        "game_type": GameType(**game_type_dict),
        "creator": User(**user_dict),
        "start_date": datetime(2024, 12, 24),
        "access_code": "0A1B2C",
        "max_participants": 4,
    }


@pytest.fixture
def patch_get_user_by_username(monkeypatch):
    def mock_get_id(_, username: str | None) -> User | None:
        return ObjectId() if username == "username" else None

    def mock_get_user(_, id: ObjectId) -> dict[str, Any]:
        return {
            "_id": id,
            "username": "username",
            "password_hash": get_password_hash("password"),
            "account_type": "standard",
            "bots": [],
            "is_banned": False,
        }

    monkeypatch.setattr(
        "app.utils.authentication.DBUser.get_id_by_username", mock_get_id
    )
    monkeypatch.setattr("app.dependencies.DBUser.get_id_by_username", mock_get_id)
    monkeypatch.setattr("app.models.user.UserCollection.get_user_by_id", mock_get_user)


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
