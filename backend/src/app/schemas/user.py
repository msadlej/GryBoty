from pydantic import BaseModel, Field
from pyobjectID import PyObjectId
from enum import Enum

from app.schemas.bot import BotModel


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class Token(BaseModel):
    """Represents a token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Represents the data stored in a token"""

    username: str | None = None


class AccountType(str, Enum):
    """Represents the type of an account"""

    STANDARD = "standard"
    PREMIUM = "premium"
    ADMIN = "admin"


class UserModel(BaseModel):
    """Represents a user"""

    id: PyObjectId = Field(alias="_id")
    username: str
    account_type: AccountType
    bots: list[BotModel] | None = None
    is_banned: bool


class UserCreate(BaseModel):
    """Represents a user creation model"""

    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=5, max_length=32)


class UserUpdate(BaseModel):
    """Represents a user update model"""

    account_type: AccountType | None = None
    is_banned: bool | None = None


class PasswordUpdate(BaseModel):
    """Represents a password update model"""

    old_password: str
    new_password: str = Field(min_length=5, max_length=32)
