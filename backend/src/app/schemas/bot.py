from app.schemas.game import GameModel
from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId


class BotModel(BaseModel):
    """Represents a bot"""

    id: MongoObjectId = Field(alias="_id")
    name: str
    game_type: GameModel | None = None
    is_validated: bool
    games_played: int
    wins: int
    losses: int
    total_tournaments: int
    tournaments_won: int
