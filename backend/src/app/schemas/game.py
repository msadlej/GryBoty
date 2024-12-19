from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId


class GameModel(BaseModel):
    """Represents a game type"""

    id: MongoObjectId = Field(alias="_id")
    name: str
    description: str
