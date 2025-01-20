from fastapi import HTTPException, status
from typing import overload, Any
from bson import ObjectId

from app.schemas.user import AccountType, User, UserUpdate
from database.main import MongoDB, User as UserCollection


class DBUser:
    """
    Represents a user model in the database.

    Attributes:
    ---
    id : ObjectId
        The unique identifier of the user.
    username : str
        The username of the user.
    password_hash : str
        The hashed password of the user.
    account_type : str
        The account type of the user.
    bots : list[ObjectId]
        The unique identifiers of the user's bots.
    is_banned : bool
        The ban status of the user.
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
        self._collection = UserCollection(db)

        if id is not None:
            self._from_id(id)
        elif data is not None:
            self._from_data(data)
        else:
            raise ValueError("DBUser must be initialized with either id or data.")

    def _from_data(self, data: dict[str, Any]) -> None:
        self.id: ObjectId = data["_id"]
        self.username: str = data["username"]
        self.password_hash: str = data["password_hash"]
        self.account_type: str = data["account_type"]
        self.bots: list[ObjectId] = data["bots"]
        self.is_banned: bool = data["is_banned"]

    def _from_id(self, user_id: ObjectId) -> None:
        data = self._collection.get_user_by_id(user_id)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User: {user_id} not found.",
            )

        self._from_data(data)

    def update_password(self, hashed_password: str) -> None:
        """
        Updates the user's password in the database.
        """

        self._collection.update_password(self.id, hashed_password)
        self._from_id(self.id)

    def update(self, user_data: UserUpdate) -> None:
        """
        Updates the user in the database.
        Raises an error if the given account type is invalid.
        """

        if user_data.account_type is AccountType.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update user to admin.",
            )

        if user_data.account_type is not None:
            self._collection.update_account_type(self.id, user_data.account_type)

        if user_data.is_banned is not None:
            self._collection.update_ban(self.id, user_data.is_banned)

        self._from_id(self.id)

    def add_bot(self, bot_id: ObjectId) -> None:
        """
        Adds a bot to the user's bots.
        """

        self._collection.add_bot(self.id, bot_id)
        self._from_id(self.id)

    def to_schema(self) -> User:
        """
        Converts the model to a User schema.
        """

        return User(
            _id=self.id,
            username=self.username,
            account_type=AccountType(self.account_type),
            is_banned=self.is_banned,
        )

    @classmethod
    def insert(cls, db: MongoDB, username, hashed_password) -> "DBUser":
        """
        Inserts a new user into the database.
        Raises an error if the user already exists.
        """

        if cls.get_id_by_username(username) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User: {username} already exists",
            )

        collection = UserCollection(db)
        user_id = collection.create_user(username, hashed_password, "standard")
        return cls(db, id=user_id)

    @staticmethod
    def get_id_by_username(db: MongoDB, username: str | None = None) -> ObjectId | None:
        """
        Retrieves a user id from the database by their username.
        Returns None if the user does not exist.
        """

        if username is None:
            return None

        collection = UserCollection(db)
        user_dict = collection.get_user_by_username(username)
        return user_dict["_id"] if user_dict is not None else None

    @staticmethod
    def get_all(db: MongoDB) -> list[User]:
        """
        Retrieves all users from the database
        """

        users = db.get_all_users()
        db_users = [DBUser(db, data=user) for user in users]
        return [db_user.to_schema() for db_user in db_users]
