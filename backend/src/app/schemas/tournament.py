from pydantic import BaseModel, Field
from pyobjectID import PyObjectId
from datetime import datetime

from app.schemas.game_type import GameType
from app.schemas.user import User
from app.schemas.bot import Bot


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class Tournament(BaseModel):
    """Represents a tournament"""

    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
    game_type: GameType
    creator: User
    start_date: datetime
    access_code: str
    max_participants: int
    winner: Bot | None = None


class TournamentCreate(BaseModel):
    """Represents a tournament creation model"""

    name: str = Field(min_length=5, max_length=32)
    description: str = Field(max_length=128)
    game_type_id: PyObjectId
    start_date: datetime = Field(gt=datetime.now())
    max_participants: int = Field(ge=2)


class TournamentUpdate(BaseModel):
    """Represents a tournament update model"""

    name: str | None = Field(min_length=5, max_length=32, default=None)
    description: str | None = Field(max_length=128, default=None)
    start_date: datetime | None = Field(gt=datetime.now(), default=None)
    max_participants: int | None = Field(ge=2, default=None)
    winner_id: PyObjectId | None = None
