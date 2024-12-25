from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId
from app.schemas.bot import BotModel
from enum import Enum


class Token(BaseModel):
    """Represents a token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Represents the data stored in a token"""

    username: str | None = None


class AccountType(Enum):
    """Represents the type of an account"""

    STANDARD = "standard"
    PREMIUM = "premium"
    ADMIN = "admin"


class UserModel(BaseModel):
    """Represents a user"""

    id: MongoObjectId = Field(alias="_id")
    username: str
    account_type: AccountType
    bots: list[BotModel] | None = None
    is_banned: bool


class UserCreate(BaseModel):
    """Represents a user creation model"""

    username: str
    password: str


class UserUpdate(BaseModel):
    """Represents a user update model"""

    old_password: str
    new_password: str
