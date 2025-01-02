from app.schemas.game import GameModel
from pydantic import BaseModel, Field
from pyobjectID import PyObjectId


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class BotModel(BaseModel):
    """Represents a bot"""

    id: PyObjectId = Field(alias="_id")
    name: str
    game_type: GameModel | None = None
    code: str
    is_validated: bool
    games_played: int
    wins: int
    losses: int
    total_tournaments: int
    tournaments_won: int
