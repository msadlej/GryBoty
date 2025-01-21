from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Literal
import secrets


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    MONGO_URI: str = "mongodb://localhost:27017"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def pwd_context(self) -> CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @property
    def oauth2_scheme(self) -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer(tokenUrl="token")


settings = Settings()
