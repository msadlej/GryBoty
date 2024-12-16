from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId
from datetime import datetime


class TournamentModel(BaseModel):
    """Represents a tournament"""

    id: MongoObjectId = Field(alias="_id")
    name: str
    description: str
    game_type: MongoObjectId
    creator: MongoObjectId
    start_date: datetime
    access_code: str
    max_participants: int
    participants: list[MongoObjectId]
    matches: list[MongoObjectId]
