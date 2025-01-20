from pydantic import BaseModel, Field
from pyobjectID import PyObjectId

from app.schemas.bot import Bot


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class Match(BaseModel):
    """Represents a match"""

    id: PyObjectId = Field(alias="_id")
    game_num: int
    players: tuple[Bot, Bot]
    moves: list[str] | None = None
    winner: Bot | None = None


class MatchCreate(BaseModel):
    """Represents a match creation request"""

    game_num: int
    player_ids: tuple[PyObjectId, PyObjectId]
