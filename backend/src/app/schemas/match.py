from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId
from app.schemas.bot import BotModel


class MatchModel(BaseModel):
    """Represents a match"""

    id: MongoObjectId = Field(alias="_id")
    game_num: int
    players: dict[str, BotModel] | None = None
    moves: list[str] | None = None
    winner: BotModel | None = None
