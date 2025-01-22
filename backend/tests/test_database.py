import pytest
import mongomock
from bson import ObjectId
from typing import Generator
from datetime import datetime, timedelta

from database.main import MongoDB, User, Bot, GameType, Tournament, Match


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


@pytest.fixture
def match_manager(mock_db: MongoDB) -> Match:
    return Match(mock_db)


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
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")
        assert bot_id is not None
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["name"] == "testbot"
        assert bot["game_type"] == game_type_id
        assert bot["is_validated"] is False
        assert bot["games_played"] == 0
        assert bot["wins"] == 0
        assert bot["losses"] == 0
        assert bot["code"] == b"print('Hello, World!')"

    def test_update_stats(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")
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
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")
        bot_manager.update_name(bot_id, "newname")
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["name"] == "newname"

    def test_validate_bot(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")
        bot_manager.validate_bot(bot_id)
        bot = bot_manager.get_bot_by_id(bot_id)
        assert bot["is_validated"] is True

    def test_get_bots_by_game_type(self, bot_manager: Bot):
        game_type_id = ObjectId()
        _ = bot_manager.create_bot("bot1", game_type_id, b"print('Hello, World!')")
        _ = bot_manager.create_bot("bot2", game_type_id, b"print('Hello, World!')")
        bots = bot_manager.get_bots_by_game_type(game_type_id)
        assert len(bots) == 2
        bot_names = [bot["name"] for bot in bots]
        assert "bot1" in bot_names
        assert "bot2" in bot_names

    def test_get_validated_bots(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id1 = bot_manager.create_bot("bot1", game_type_id, b"print('Hello, World!')")
        _ = bot_manager.create_bot("bot2", game_type_id, b"print('Hello, World!')")
        bot_manager.validate_bot(bot_id1)
        validated_bots = bot_manager.get_validated_bots()
        assert len(validated_bots) == 1
        assert validated_bots[0]["name"] == "bot1"

    def test_get_bot_stats(self, bot_manager: Bot):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")
        bot_manager.update_stats(bot_id, True)
        bot_manager.update_stats(bot_id, False)
        stats = bot_manager.get_bot_stats(bot_id)
        assert stats["games_played"] == 2
        assert stats["wins"] == 1
        assert stats["losses"] == 1

    def test_get_all_bots(self, bot_manager: Bot):
        game_type_id = ObjectId()
        _ = bot_manager.create_bot("bot1", game_type_id, b"print('Hello, World!')")
        _ = bot_manager.create_bot("bot2", game_type_id, b"print('Hello, World!')")
        bots = bot_manager.get_all_bots()
        assert len(bots) == 2
        bot_names = [bot["name"] for bot in bots]
        assert "bot1" in bot_names
        assert "bot2" in bot_names

    def test_get_owner(self, bot_manager: Bot, user_manager: User):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")

        user_id = user_manager.create_user(
            username="testuser",
            password_hash="hashedpassword123",
            account_type="standard"
        )

        user_manager.add_bot(user_id, bot_id)
        owner = bot_manager.get_owner(bot_id)
        assert owner is not None
        assert owner["username"] == "testuser"
        assert owner["_id"] == user_id
        assert bot_id in owner["bots"]

        non_existent_bot_id = ObjectId()
        owner = bot_manager.get_owner(non_existent_bot_id)
        assert owner is None

    def test_delete_bot_all_dependencies(self, bot_manager: Bot, user_manager: User, tournament_manager: Tournament, match_manager: Match):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")
        opponent_id = bot_manager.create_bot("opponent", game_type_id, b"print('Hello, World!')")

        user_id = user_manager.create_user("testuser", "hashedpassword123", "standard")
        user_manager.add_bot(user_id, bot_id)

        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            game_type_id,
            user_id,
            datetime.now() + timedelta(days=1),
            "ACCESS123",
            10
        )
        tournament_manager.add_participant(tournament_id, bot_id)
        tournament_manager.add_participant(tournament_id, opponent_id)
        match_id1 = match_manager.create_match(1, bot_id, opponent_id)
        match_id2 = match_manager.create_match(2, opponent_id, bot_id)
        tournament_manager.add_match(tournament_id, match_id1)
        tournament_manager.add_match(tournament_id, match_id2)
        tournament_manager.set_winner(tournament_id, bot_id)

        result = bot_manager.delete_bot(bot_id)
        assert result is True
        assert bot_manager.get_bot_by_id(bot_id) is None

        user = user_manager.get_user_by_id(user_id)
        assert bot_id not in user["bots"]

        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert bot_id not in tournament["participants"]
        assert tournament["winner"] is None

        matches = match_manager.get_matches_by_bot(bot_id)
        assert len(matches) == 0

        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert match_id1 not in tournament["matches"]
        assert match_id2 not in tournament["matches"]

        assert bot_manager.get_bot_by_id(opponent_id) is not None

    def test_get_tournaments_won(self, bot_manager: Bot, tournament_manager: Tournament):
        game_type_id = ObjectId()
        bot_id = bot_manager.create_bot("testbot", game_type_id, b"print('Hello, World!')")

        creator_id = ObjectId()
        tournament_id1 = tournament_manager.create_tournament(
            "Tournament 1",
            "Description 1",
            game_type_id,
            creator_id,
            datetime.now() + timedelta(days=1),
            "ACCESS123",
            10
        )
        tournament_id2 = tournament_manager.create_tournament(
            "Tournament 2",
            "Description 2",
            game_type_id,
            creator_id,
            datetime.now() + timedelta(days=2),
            "ACCESS456",
            10
        )
        tournament_id3 = tournament_manager.create_tournament(
            "Tournament 3",
            "Description 3",
            game_type_id,
            creator_id,
            datetime.now() + timedelta(days=3),
            "ACCESS789",
            10
        )

        tournament_manager.set_winner(tournament_id1, bot_id)
        bot_stats = bot_manager.get_bot_stats(bot_id)
        assert bot_stats["tournaments_won"] == 1
        tournament_manager.set_winner(tournament_id2, bot_id)
        bot_stats = bot_manager.get_bot_stats(bot_id)
        assert bot_stats["tournaments_won"] == 2
        tournament_manager.set_winner(tournament_id3, ObjectId())
        bot_stats = bot_manager.get_bot_stats(bot_id)
        assert bot_stats["tournaments_won"] == 2

        won_tournaments = bot_manager.get_tournaments_won(bot_id)

        assert len(won_tournaments) == 2
        tournament_names = {t["name"] for t in won_tournaments}
        assert "Tournament 1" in tournament_names
        assert "Tournament 2" in tournament_names
        assert "Tournament 3" not in tournament_names


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
            8,
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
            2,
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
            8,
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
            8,
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
            8,
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
            8,
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
            8,
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
            2,
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
            8,
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
            8,
        )
        _ = tournament_manager.create_tournament(
            "Tournament 2",
            "Description 2",
            game_type_id,
            ObjectId(),
            datetime.now(),
            "ACCESS2",
            8,
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
            8,
        )
        _ = tournament_manager.create_tournament(
            "Tournament 2",
            "Description 2",
            ObjectId(),
            creator_id,
            datetime.now(),
            "ACCESS2",
            8,
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
            8,
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
            8,
        )
        _ = tournament_manager.create_tournament(
            "Past Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            past_date,
            "ACCESS2",
            8,
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
            8,
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
            8,
        )
        tournament_manager.add_participant(tournament_id, bot_id)

        tournaments = tournament_manager.get_tournaments_by_bot_id(bot_id)
        assert len(tournaments) == 1
        assert tournaments[0]["name"] == "Test Tournament"

    def test_set_winner(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8,
        )
        bot_id = ObjectId()
        tournament_manager.set_winner(tournament_id, bot_id)

        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert tournament["winner"] == bot_id

    def test_get_winner(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8,
        )
        bot_id = ObjectId()
        tournament_manager.set_winner(tournament_id, bot_id)

        winner_id = tournament_manager.get_winner(tournament_id)
        assert winner_id == bot_id

    def test_get_winner_no_winner(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8,
        )
        winner_id = tournament_manager.get_winner(tournament_id)
        assert winner_id is None

    def test_remove_participant(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8,
        )
        bot_id = ObjectId()
        tournament_manager.add_participant(tournament_id, bot_id)

        success = tournament_manager.remove_participant(tournament_id, bot_id)
        assert success is True

        tournament = tournament_manager.get_tournament_by_id(tournament_id)
        assert bot_id not in tournament["participants"]

    def test_remove_nonexistent_participant(self, tournament_manager: Tournament):
        tournament_id = tournament_manager.create_tournament(
            "Test Tournament",
            "Description",
            ObjectId(),
            ObjectId(),
            datetime.now(),
            "ACCESS123",
            8,
        )
        bot_id = ObjectId()

        success = tournament_manager.remove_participant(tournament_id, bot_id)
        assert success is False


class TestMatch:
    def test_create_match(self, match_manager: Match):
        bot1_id = ObjectId()
        bot2_id = ObjectId()
        match_id = match_manager.create_match(1, bot1_id, bot2_id)
        assert match_id is not None
        match = match_manager.get_match_by_id(match_id)
        assert match["game_num"] == 1
        assert match["players"][0] == bot1_id
        assert match["players"][1] == bot2_id
        assert match["moves"] == []
        assert match["winner"] is None

    def test_add_move(self, match_manager: Match):
        match_id = match_manager.create_match(1, ObjectId(), ObjectId())
        match_manager.add_move(match_id, "e2e4")
        match = match_manager.get_match_by_id(match_id)
        assert "e2e4" in match["moves"]

    def test_set_winner(self, match_manager: Match):
        bot1_id = ObjectId()
        bot2_id = ObjectId()
        match_id = match_manager.create_match(1, bot1_id, bot2_id)
        match_manager.set_winner(match_id, bot1_id)
        match = match_manager.get_match_by_id(match_id)
        assert match["winner"] == bot1_id

    def test_get_matches_by_bot(self, match_manager: Match):
        bot1_id = ObjectId()
        bot2_id = ObjectId()
        _ = match_manager.create_match(1, bot1_id, bot2_id)
        _ = match_manager.create_match(2, bot2_id, bot1_id)

        matches = match_manager.get_matches_by_bot(bot1_id)
        assert len(matches) == 2
        game_nums = [match["game_num"] for match in matches]
        assert 1 in game_nums
        assert 2 in game_nums

    def test_get_match_moves(self, match_manager: Match):
        match_id = match_manager.create_match(1, ObjectId(), ObjectId())
        match_manager.add_move(match_id, "e2e4")
        match_manager.add_move(match_id, "e7e5")

        moves = match_manager.get_match_moves(match_id)
        assert len(moves) == 2
        assert moves[0] == "e2e4"
        assert moves[1] == "e7e5"

    def test_get_matches_by_winner(self, match_manager: Match):
        bot1_id = ObjectId()
        bot2_id = ObjectId()
        match_id1 = match_manager.create_match(1, bot1_id, bot2_id)
        match_id2 = match_manager.create_match(2, bot2_id, bot1_id)

        match_manager.set_winner(match_id1, bot1_id)
        match_manager.set_winner(match_id2, bot1_id)

        matches = match_manager.get_matches_by_winner(bot1_id)
        assert len(matches) == 2
        game_nums = [match["game_num"] for match in matches]
        assert 1 in game_nums
        assert 2 in game_nums
