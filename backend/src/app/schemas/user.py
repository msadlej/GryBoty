from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId
from enum import Enum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AccountType(Enum):
    STANDARD: str = "standard"
    PREMIUM: str = "premium"
    ADMIN: str = "admin"


class UserModel(BaseModel):
    id: MongoObjectId = Field(alias="_id")
    username: str
    password_hash: str
    account_type: AccountType
    bots: list[MongoObjectId]
    is_banned: bool


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    password_hash: str | None = None
    account_type: AccountType | None = None
    bots: list[MongoObjectId] | None = None
    is_banned: bool | None = None
