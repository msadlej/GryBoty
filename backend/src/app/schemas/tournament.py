from pydantic import BaseModel, Field
from pyobjectID import PyObjectId
from datetime import datetime

from app.schemas.match import MatchModel
from app.schemas.game import GameModel
from app.schemas.user import UserModel
from app.schemas.bot import BotModel


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class TournamentModel(BaseModel):
    """Represents a tournament"""

    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
    game_type: GameModel
    creator: UserModel
    start_date: datetime
    access_code: str
    max_participants: int
    participants: list[BotModel] | None = None
    matches: list[MatchModel] | None = None


class TournamentCreate(BaseModel):
    """Represents a tournament creation model"""

    name: str = Field(min_length=5, max_length=32)
    description: str = Field(max_length=128)
    game_type: PyObjectId
    start_date: datetime
    max_participants: int = Field(ge=2)


class TournamentUpdate(BaseModel):
    """Represents a tournament update model"""

    name: str | None = Field(min_length=5, max_length=32, default=None)
    description: str | None = Field(max_length=128, default=None)
    start_date: datetime | None = None
    max_participants: int | None = Field(ge=2, default=None)
