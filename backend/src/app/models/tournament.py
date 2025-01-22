from fastapi import HTTPException, status
from typing import overload, Any
from datetime import datetime
from bson import ObjectId
import random
import string

from app.schemas.tournament import Tournament, TournamentCreate, TournamentUpdate
from database.main import MongoDB, Tournament as TournamentCollection
from app.schemas.match import Match, MatchCreate
from app.schemas.user import AccountType, User
from app.schemas.bot import Bot
import app.models.game_type as G
import app.models.match as M
import app.models.user as U
import app.models.bot as B


class DBTournament:
    """
    Represents a tournament model in the database.

    Attributes:
    ---
    id : ObjectId
        The unique identifier of the tournament.
    name : str
        The name of the tournament.
    description : str
        The description of the tournament.
    game_type : ObjectId
        The game type the tournament is associated with.
    creator : ObjectId
        The unique identifier of the creator of the tournament.
    start_date : datetime
        The start date of the tournament.
    access_code : str
        The access code of the tournament.
    max_participants : int
        The maximum number of participants in the tournament.
    participants : list[ObjectId]
        The unique identifiers of the participants in the tournament.
    matches : list[ObjectId]
        The unique identifiers of the matches in the tournament.
    winner : ObjectId
        The unique identifier of the winner of the tournament.
    """

    @overload
    def __init__(self, db: MongoDB, /, *, id: ObjectId) -> None: ...

    @overload
    def __init__(self, db: MongoDB, /, *, data: dict[str, Any]) -> None: ...

    def __init__(
        self,
        db: MongoDB,
        /,
        *,
        id: ObjectId | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        self._db = db
        self._collection = TournamentCollection(db)

        if id is not None:
            self._from_id(id)
        elif data is not None:
            self._from_data(data)
        else:
            raise ValueError("DBTournament must be initialized with either id or data.")

    def _from_data(self, data: dict[str, Any]) -> None:
        self.id: ObjectId = data["_id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.game_type: ObjectId = data["game_type"]
        self.creator: ObjectId = data["creator"]
        self.start_date: datetime = data["start_date"]
        self.access_code: str = data["access_code"]
        self.max_participants: int = data["max_participants"]
        self.participants: list[ObjectId] = data["participants"]
        self.matches: list[ObjectId] = data["matches"]
        self.winner: ObjectId | None = data["winner"]

    def _from_id(self, tournament_id: ObjectId) -> None:
        data = self._collection.get_tournament_by_id(tournament_id)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tournament: {tournament_id} not found.",
            )

        self._from_data(data)

    def check_creator(self, user: User) -> bool:
        """
        Checks if the user is the creator of the tournament or an admin.
        """

        is_admin: bool = user.account_type is AccountType.ADMIN
        is_creator: bool = user.id == self.creator

        return is_creator or is_admin

    def check_access(self, user: User) -> bool:
        """
        Checks if the user has access to the tournament.
        """

        db_user = U.DBUser(self._db, id=user.id)

        is_admin: bool = user.account_type is AccountType.ADMIN
        is_creator: bool = user.id == self.creator
        is_participant: bool = any(
            bot_id in self.participants for bot_id in db_user.bots
        )

        return any((is_admin, is_creator, is_participant))

    def get_participants(self) -> list[Bot]:
        """
        Retrieves all bots from the database that participate in the tournament.
        """

        db_bots = [B.DBBot(self._db, id=bot_id) for bot_id in self.participants]
        return [db_bot.to_schema() for db_bot in db_bots]

    def get_matches(self) -> list[Match]:
        """
        Retrieves all matches from the database that belong to a specific tournament.
        """

        db_matches = [M.DBMatch(self._db, id=match_id) for match_id in self.matches]

        return [db_match.to_schema() for db_match in db_matches]

    def update(self, tournament_data: TournamentUpdate) -> None:
        """
        Updates the tournament in the database.
        """

        if self._is_finished():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tournament: {self.id} is already finished.",
            )

        if tournament_data.name is not None:
            self._collection.update_name(self.id, tournament_data.name)

        if tournament_data.description is not None:
            self._collection.update_description(self.id, tournament_data.description)

        if tournament_data.start_date is not None:
            self._collection.update_start_date(self.id, tournament_data.start_date)

        if tournament_data.max_participants is not None:
            self._collection.update_max_participants(
                self.id, tournament_data.max_participants
            )

        self._from_id(self.id)

    def set_winner(self, winner_id: ObjectId) -> None:
        """
        Sets the winner of the tournament.
        """

        db_winner = B.DBBot(self._db, id=winner_id)
        db_winner.update_tournament_wins()

        self._collection.set_winner(self.id, winner_id)
        self._from_id(self.id)

    def add_participant(self, bot_id: ObjectId) -> None:
        """
        Adds a bot to the tournament.
        """

        if self._is_finished():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tournament: {self.id} is already finished.",
            )

        db_bot = B.DBBot(self._db, id=bot_id)
        if db_bot.game_type != self.game_type:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Bot: {bot_id} does not match the game type of the tournament.",
            )
        if not db_bot.is_validated:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Bot: {bot_id} is not validated.",
            )

        owner = db_bot.get_owner()
        if self._is_user_participant(owner.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User: {owner.id} already has a bot in the tournament",
            )

        success = self._collection.add_participant(self.id, bot_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tournament: {self.id} is already full.",
            )

        self._from_id(self.id)

    def remove_participant(self, bot_id: ObjectId) -> None:
        """
        Removes a bot from the tournament.
        """

        if self._is_finished():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tournament: {self.id} is already finished.",
            )

        success = self._collection.remove_participant(self.id, bot_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bot: {bot_id} is not a participant in the tournament.",
            )

        self._from_id(self.id)

    def add_match(self, match_id: ObjectId) -> None:
        """
        Adds a match to the tournament.
        """

        self._collection.add_match(self.id, match_id)
        self._from_id(self.id)

    def run(self) -> None:
        """
        Starts the tournament.
        Creates the first round of matches.
        Adds an example bot to the tournament if there are too few participants.
        """

        if self._is_finished():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tournament: {self.id} is already finished.",
            )

        participants = self._fill_tournament()
        random.shuffle(participants)
        for i in range(len(participants) // 2):
            bot_0 = participants[2 * i]
            bot_1 = participants[2 * i + 1]

            match_data = MatchCreate(game_num=i, player_0_id=bot_0, player_1_id=bot_1)
            M.DBMatch.insert(self._db, self.id, match_data)

        self._collection.update_start_date(self.id, datetime.now())
        self._from_id(self.id)

    def to_schema(self) -> Tournament:
        """
        Converts the model to a Tournament schema.
        """

        db_game_type = G.DBGameType(self._db, id=self.game_type)
        game_type = db_game_type.to_schema()

        db_creator = U.DBUser(self._db, id=self.creator)
        creator = db_creator.to_schema()

        db_winner = B.DBBot(self._db, id=self.winner) if self.winner else None
        winner = db_winner.to_schema() if db_winner else None

        return Tournament(
            _id=self.id,
            name=self.name,
            description=self.description,
            game_type=game_type,
            creator=creator,
            start_date=self.start_date,
            access_code=self.access_code,
            max_participants=self.max_participants,
            winner=winner,
        )

    @classmethod
    def insert(
        cls, db: MongoDB, creator: User, tournament_data: TournamentCreate
    ) -> "DBTournament":
        """
        Inserts a new tournament into the database.
        Returns the created tournament.
        """

        G.DBGameType(db, id=tournament_data.game_type_id)

        access_code = cls._generate_access_code()
        i = 0
        while cls.get_id_by_access_code(db, access_code) is not None:
            access_code = cls._generate_access_code()
            i += 1

            if i > 9:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate unique access code.",
                )

        collection = TournamentCollection(db)
        tournament_id = collection.create_tournament(
            tournament_data.name,
            tournament_data.description,
            tournament_data.game_type_id,
            creator.id,
            tournament_data.start_date,
            access_code,
            tournament_data.max_participants,
        )

        return cls(db, id=tournament_id)

    @staticmethod
    def get_id_by_access_code(db: MongoDB, access_code: str) -> ObjectId | None:
        """
        Retrieves a tournament ID from the database by its access code.
        Returns None if the access code does not exist.
        """

        collection = TournamentCollection(db)
        tournament = collection.get_tournament_by_access_code(access_code)

        return tournament["_id"] if tournament else None

    @staticmethod
    def get_all(db: MongoDB) -> list[Tournament]:
        """
        Retrieves all tournaments from the database.
        """

        collection = TournamentCollection(db)
        tournaments = collection.get_all_tournaments()
        db_tournaments = [
            DBTournament(db, data=tournament) for tournament in tournaments
        ]

        return [db_tournament.to_schema() for db_tournament in db_tournaments]

    def _is_user_participant(self, user_id: ObjectId) -> bool:
        """
        Checks if a user is a participant in the tournament.
        """

        db_user = U.DBUser(self._db, id=user_id)
        return any(bot_id in self.participants for bot_id in db_user.bots)

    def _is_finished(self) -> bool:
        """
        Checks if the tournament is finished.
        """

        return self.start_date < datetime.now()

    def _get_example_bot(self) -> Bot:
        """
        Retrieves an example bot for the tournament.
        """

        admin_id = U.DBUser.get_id_by_username(self._db, "admin")
        if admin_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found.",
            )

        db_admin = U.DBUser(self._db, id=admin_id)
        example_bots = db_admin.get_bots()
        example_bot = None
        for bot in example_bots:
            if bot.game_type.id == self.game_type:
                example_bot = bot
                break

        if example_bot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Example bot not found for game type: {self.game_type}",
            )

        return example_bot

    def _fill_tournament(self) -> list[ObjectId]:
        """
        Fills the tournament with example bots if there are too few participants.
        Returns the modified list of participants.
        """

        n_participants = len(self.participants)
        next_power = 1
        while next_power < n_participants:
            next_power *= 2
        bots_needed = next_power - n_participants

        participants = self.participants
        if bots_needed > 0:
            example_bot = self._get_example_bot()
            self.add_participant(example_bot.id)

            for _ in range(bots_needed):
                participants.append(example_bot.id)

        return participants

    @staticmethod
    def _generate_access_code(length: int = 6) -> str:
        """
        Generates a random access code with digits and capital letters.
        """

        characters = string.ascii_uppercase + string.digits
        return "".join(random.choice(characters) for _ in range(length))
