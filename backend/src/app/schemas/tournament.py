from app.schemas.match import MatchModel
from app.schemas.game import GameModel
from app.schemas.user import UserModel
from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId
from app.schemas.bot import BotModel
from datetime import datetime


class TournamentModel(BaseModel):
    """Represents a tournament"""

    id: MongoObjectId = Field(alias="_id")
    name: str
    description: str
    game_type: GameModel | None = None
    creator: UserModel | None = None
    start_date: datetime
    access_code: str
    max_participants: int
    participants: list[BotModel] | None = None
    matches: list[MatchModel] | None = None
