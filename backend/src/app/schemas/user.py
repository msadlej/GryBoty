from pydantic import BaseModel
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


class User(BaseModel):
    username: str
    account_type: AccountType
    is_banned: bool | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    password: str


class DBUser(User):
    id: str
    password_hash: str
