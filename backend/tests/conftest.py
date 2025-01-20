from contextlib import contextmanager
from datetime import datetime
from bson import ObjectId
from typing import Any
import mongomock
import pytest

from app.schemas.game_type import GameType, GameTypeCreate
from app.utils.authentication import get_password_hash
from app.models.game_type import DBGameType
from app.models.user import DBUser
from database.main import MongoDB
from app.schemas.user import User
from app.models.bot import DBBot
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
def bot_dict(game_type_dict, user_dict):
    return {
        "_id": ObjectId(),
        "name": "Test Bot",
        "game_type": GameType(**game_type_dict),
        "code": b"print('Hello, World!')",
        "is_validated": True,
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "total_tournaments": 0,
        "tournaments_won": 0,
        "owner": User(**user_dict),
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
def tournament_dict(game_type_dict, user_dict, bot_dict):
    return {
        "_id": ObjectId(),
        "name": "Test Tournament",
        "description": "Test Description",
        "game_type": GameType(**game_type_dict),
        "creator": User(**user_dict),
        "start_date": datetime(2024, 12, 24),
        "access_code": "0A1B2C",
        "max_participants": 4,
        "winner": Bot(**bot_dict),
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


@pytest.fixture
def insert_game_type(db_connection, game_type_dict):
    game_type = GameTypeCreate(**game_type_dict)
    db_game_type = DBGameType.insert(db_connection, game_type)

    return db_game_type


@pytest.fixture
def insert_user(db_connection, user_dict):
    db_user = DBUser.insert(
        db_connection, user_dict["username"], user_dict["password_hash"]
    )

    return db_user


@pytest.fixture
def insert_bot(monkeypatch, insert_game_type, insert_user, db_connection, bot_dict):
    monkeypatch.setattr("app.models.bot.conn.validate_bot", lambda x, y: True)

    db_game_type = insert_game_type
    db_user = insert_user
    db_bot = DBBot.insert(
        db_connection,
        db_user.to_schema(),
        bot_dict["name"],
        db_game_type.id,
        bot_dict["code"],
    )

    return db_game_type, db_user, db_bot
