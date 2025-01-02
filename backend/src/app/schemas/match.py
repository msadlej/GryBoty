from pydantic import BaseModel, Field
from pyobjectID import PyObjectId
from app.schemas.bot import BotModel


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class MatchModel(BaseModel):
    """Represents a match"""

    id: PyObjectId = Field(alias="_id")
    game_num: int
    players: dict[str, BotModel] | None = None
    moves: list[str] | None = None
    winner: BotModel | None = None
