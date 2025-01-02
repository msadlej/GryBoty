from pydantic import BaseModel, Field
from pyobjectID import PyObjectId


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class GameModel(BaseModel):
    """Represents a game type"""

    id: PyObjectId = Field(alias="_id")
    name: str
    description: str
