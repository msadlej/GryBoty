import pytest
import mongomock
from bson import ObjectId
from typing import Generator

from database.main import MongoDB, User, Bot


@pytest.fixture
def mock_db() -> Generator[MongoDB, None, None]:
    client = mongomock.MongoClient()
    db = MongoDB()
    db.client = client
    db.db = client.pzsp_database
    yield db
    client.close()


@pytest.fixture
def user_manager(mock_db: MongoDB) -> User:
    return User(mock_db)


@pytest.fixture
def bot_manager(mock_db: MongoDB) -> Bot:
    return Bot(mock_db)


class TestUser:
    def test_create_user(self, user_manager: User):
        user_id = user_manager.create_user("testuser", "hash123", "standard")
        assert user_id is not None
        user = user_manager.get_user_by_id(user_id)
        assert user["username"] == "testuser"
        assert user["password_hash"] == "hash123"
        assert user["account_type"] == "standard"
        assert user["is_banned"] is False
        assert user["bots"] == []

    def test_add_bot(self, user_manager: User):
        user_id = user_manager.create_user("testuser", "hash123", "standard")
        bot_id = ObjectId()
        user_manager.add_bot(user_id, bot_id)
        user = user_manager.get_user_by_id(user_id)
        assert bot_id in user["bots"]

    def test_update_ban(self, user_manager: User):
        user_id = user_manager.create_user("testuser", "hash123", "standard")
        user_manager.update_ban(user_id, True)
        user = user_manager.get_user_by_id(user_id)
        assert user["is_banned"] is True

    def test_update_account_type(self, user_manager: User):
        user_id = user_manager.create_user("testuser", "hash123", "standard")
        user_manager.update_account_type(user_id, "premium")
        user = user_manager.get_user_by_id(user_id)
        assert user["account_type"] == "premium"

    def test_update_password(self, user_manager: User):
        user_id = user_manager.create_user("testuser", "hash123", "standard")
        user_manager.update_password(user_id, "newhash123")
        user = user_manager.get_user_by_id(user_id)
        assert user["password_hash"] == "newhash123"

    def test_get_user_by_username(self, user_manager: User):
        user_manager.create_user("testuser", "hash123", "standard")
        user = user_manager.get_user_by_username("testuser")
        assert user is not None
        assert user["username"] == "testuser"

    def test_get_user_bots(self, user_manager: User):
        user_id = user_manager.create_user("testuser", "hash123", "standard")
        bot_id1 = ObjectId()
        bot_id2 = ObjectId()
        user_manager.add_bot(user_id, bot_id1)
        user_manager.add_bot(user_id, bot_id2)
        bots = user_manager.get_user_bots(user_id)
        assert len(bots) == 2
        assert bot_id1 in bots
        assert bot_id2 in bots

    def test_get_all_users(self, user_manager: User):
        _ = user_manager.create_user("user1", "hash1", "standard")
        _ = user_manager.create_user("user2", "hash2", "premium")
        users = user_manager.get_all_users()
        assert len(users) == 2
        usernames = [user["username"] for user in users]
        assert "user1" in usernames
        assert "user2" in usernames


class TestBot:
    def test_create_bot(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id)
        assert bot_id is not None
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["name"] == "testbot"
        assert bot["game_type"] == game_type_id
        assert bot["is_validated"] is False
        assert bot["games_played"] == 0
        assert bot["wins"] == 0
        assert bot["losses"] == 0

    def test_add_code_path(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id)
        bot_manager.add_code_path(bot_id, "/path/to/code")
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["code_path"] == "/path/to/code"

    def test_update_stats(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id)
        bot_manager.update_stats(bot_id, True)
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["games_played"] == 1
        assert bot["wins"] == 1
        assert bot["losses"] == 0

        bot_manager.update_stats(bot_id, False)
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["games_played"] == 2
        assert bot["wins"] == 1
        assert bot["losses"] == 1

    def test_update_name(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id)
        bot_manager.update_name(bot_id, "newname")
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["name"] == "newname"

    def test_validate_bot(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id)
        bot_manager.validate_bot(bot_id)
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["is_validated"] is True

    def test_get_bots_by_game_type(self, bot_manager: Bot):
        game_type_id = ObjectId()
        _ = bot_manager.create_bot("bot1", game_type_id)
        _ = bot_manager.create_bot("bot2", game_type_id)
        bots = bot_manager.get_bots_by_game_type(game_type_id)
        assert len(bots) == 2
        bot_names = [bot["name"] for bot in bots]
        assert "bot1" in bot_names
        assert "bot2" in bot_names

    def test_get_validated_bots(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id1 = bot_manager.create_bot("bot1", game_type_id)
        _ = bot_manager.create_bot("bot2", game_type_id)
        bot_manager.validate_bot(bot_id1)
        validated_bots = bot_manager.get_validated_bots()
        assert len(validated_bots) == 1
        assert validated_bots[0]["name"] == "bot1"

    def test_get_bot_stats(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id)
        bot_manager.update_stats(bot_id, True)
        bot_manager.update_stats(bot_id, False)
        stats = bot_manager.get_bot_stats(bot_id)
        assert stats["games_played"] == 2
        assert stats["wins"] == 1
        assert stats["losses"] == 1

    def test_get_all_bots(self, bot_manager: Bot):
        game_type_id = ObjectId()
        _ = bot_manager.create_bot("bot1", game_type_id)
        _ = bot_manager.create_bot("bot2", game_type_id)
        bots = bot_manager.get_all_bots()
        assert len(bots) == 2
        bot_names = [bot["name"] for bot in bots]
        assert "bot1" in bot_names
        assert "bot2" in bot_names
