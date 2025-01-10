from pydantic import BaseModel, Field
from pyobjectID import PyObjectId

from app.schemas.game import GameModel


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class BotModel(BaseModel):
    """Represents a bot"""

    id: PyObjectId = Field(alias="_id")
    name: str
    game_type: GameModel | None = None
    code_path: str
    is_validated: bool
    games_played: int
    wins: int
    losses: int
    total_tournaments: int
    tournaments_won: int


class BotUpdate(BaseModel):
    """Represents a bot update"""

    name: str | None = Field(min_length=3, max_length=16, default=None)
