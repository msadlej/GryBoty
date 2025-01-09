import pytest
import mongomock
from bson import ObjectId
from typing import Generator
from datetime import datetime

from database.main import MongoDB, User, Bot, GameType, Tournament


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


@pytest.fixture
def game_type_manager(mock_db: MongoDB) -> GameType:
    return GameType(mock_db)


@pytest.fixture
def tournament_manager(mock_db: MongoDB) -> Tournament:
    return Tournament(mock_db)


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


class TestGameType:
    def test_create_game_type(self, game_type_manager: GameType):
        game_type_id = game_type_manager.create_game_type("Chess", "Classic chess game")
        assert game_type_id is not None
        game_type = game_type_manager.get_game_type_by_id(game_type_id)
        assert game_type["name"] == "Chess"
        assert game_type["description"] == "Classic chess game"

    def test_get_game_type_by_name(self, game_type_manager: GameType):
        game_type_manager.create_game_type("Chess", "Classic chess game")
        game_type = game_type_manager.get_game_type_by_name("Chess")
        assert game_type is not None
        assert game_type["name"] == "Chess"
        assert game_type["description"] == "Classic chess game"

    def test_get_all_game_types(self, game_type_manager: GameType):
        game_type_manager.create_game_type("Chess", "Classic chess game")
        game_type_manager.create_game_type("Checkers", "Classic checkers game")
        game_types = game_type_manager.get_all_game_types()
        assert len(game_types) == 2
        game_names = [gt["name"] for gt in game_types]
        assert "Chess" in game_names
        assert "Checkers" in game_names


class TestTournament:
    def test_create_tournament(self, tournament_manager: Tournament):
        start_date = datetime.now()
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            start_date,
            "ACCESS123",
            8
        )
        assert tournament_id is not None
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert tournament["name"] == "Test Tournament"
        assert tournament["max_participants"] == 8
        assert tournament["participants"] == []

    def test_add_participant(self, tournament_manager: Tournament):
        start_date = datetime.now()
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            start_date,
            "ACCESS123",
            2
        )
        bot_id = ObjectId()
        success = tournament_manager.add_participant(tournament_id, bot_id)
        assert success is True
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert bot_id in tournament["participants"]

    def test_add_match(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        match_id = ObjectId()
        tournament_manager.add_match(tournament_id, match_id)
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert match_id in tournament["matches"]

    def test_update_name(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        tournament_manager.update_name(tournament_id, "New Name")
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert tournament["name"] == "New Name"

    def test_update_description(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        tournament_manager.update_description(tournament_id, "New Description")
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert tournament["description"] == "New Description"

    def test_update_start_date(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        new_date = datetime(2050, 12, 31)
        tournament_manager.update_start_date(tournament_id, new_date)
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert tournament["start_date"] == new_date

    def test_update_max_participants(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        success = tournament_manager.update_max_participants(tournament_id, 10)
        assert success is True
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert tournament["max_participants"] == 10

    def test_update_max_participants_fail(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            2
        )
        tournament_manager.add_participant(tournament_id, ObjectId())
        tournament_manager.add_participant(tournament_id, ObjectId())
        success = tournament_manager.update_max_participants(tournament_id, 1)
        assert success is False
        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert tournament["max_participants"] == 2

    def test_get_tournament_matches(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Test Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        match_id1 = ObjectId()
        match_id2 = ObjectId()
        tournament_manager.add_match(tournament_id, match_id1)
        tournament_manager.add_match(tournament_id, match_id2)
        matches = tournament_manager.get_tournament_matches(tournament_id)
        assert len(matches) == 2
        assert match_id1 in matches
        assert match_id2 in matches

    def test_get_tournaments_by_game_type(self, tournament_manager: Tournament):
        game_type_id = ObjectId()
        _ = tournament_manager.create_tournament(
            "Tournament 1",
            "Description 1",
            game_type_id,
            ObjectId(),
            datetime.now(),
            "ACCESS1",
            8
        )
        _ = tournament_manager.create_tournament(
            "Tournament 2",
            "Description 2",
            game_type_id,
            ObjectId(),
            datetime.now(),
            "ACCESS2",
            8
        )
        tournaments = tournament_manager.get_tournaments_by_game_type(game_type_id)
        assert len(tournaments) == 2
        tournament_names = [t["name"] for t in tournaments]
        assert "Tournament 1" in tournament_names
        assert "Tournament 2" in tournament_names

    def test_get_tournaments_by_creator(self, tournament_manager: Tournament):
        creator_id = ObjectId()
        _ = tournament_manager.create_tournament(
            "Tournament 1",
            "Description 1",
            ObjectId(),
            creator_id,
            datetime.now(),
            "ACCESS1",
            8
        )
        _ = tournament_manager.create_tournament(
            "Tournament 2",
            "Description 2",
            ObjectId(),
            creator_id,
            datetime.now(),
            "ACCESS2",
            8
        )
        tournaments = tournament_manager.get_tournaments_by_creator(creator_id)
        assert len(tournaments) == 2
        tournament_names = [t["name"] for t in tournaments]
        assert "Tournament 1" in tournament_names
        assert "Tournament 2" in tournament_names

    def test_get_tournament_by_access_code(self, tournament_manager: Tournament):
        _ = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        tournament = tournament_manager.get_tournament_by_access_code("ACCESS123")
        assert tournament is not None
        assert tournament["name"] == "Test Tournament"

    def test_get_upcoming_tournaments(self, tournament_manager: Tournament):
        future_date = datetime(2050, 1, 1)
        past_date = datetime(2023, 1, 1)

        _ = tournament_manager.create_tournament(
            "Future Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            future_date,
            "ACCESS1",
            8
        )
        _ = tournament_manager.create_tournament(
            "Past Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            past_date,
            "ACCESS2",
            8
        )

        upcoming = tournament_manager.get_upcoming_tournaments()
        assert len(upcoming) == 1
        assert upcoming[0]["name"] == "Future Tournament"

    def test_get_tournament_participants(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        bot_id1 = ObjectId()
        bot_id2 = ObjectId()
        tournament_manager.add_participant(tournament_id, bot_id1)
        tournament_manager.add_participant(tournament_id, bot_id2)

        participants = tournament_manager.get_tournament_participants(tournament_id)
        assert len(participants) == 2
        assert bot_id1 in participants
        assert bot_id2 in participants

    def test_get_tournaments_by_bot_id(self, tournament_manager: Tournament):
        bot_id = ObjectId()
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8
        )
        tournament_manager.add_participant(tournament_id, bot_id)

        tournaments = tournament_manager.get_tournaments_by_bot_id(bot_id)
        assert len(tournaments) == 1
        assert tournaments[0]["name"] == "Test Tournament"
