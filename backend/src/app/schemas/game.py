from pydantic import BaseModel, Field
from pyobjectID import PyObjectId


BaseModel.model_config["json_encoders"] = {PyObjectId: lambda v: str(v)}


class GameTypeModel(BaseModel):
    """Represents a game type"""

    id: PyObjectId = Field(alias="_id")
    name: str
    description: str


class GameTypeCreate(BaseModel):
    """Represents a game type crration request"""

    name: str = Field(min_length=5, max_length=32)
    description: str = Field(max_length=128)
