import pytest
import mongomock
from bson import ObjectId
from typing import Generator

from database.main import MongoDB, User


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
