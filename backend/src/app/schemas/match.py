from pydantic import BaseModel, Field
from pyobjectID import MongoObjectId


class MatchModel(BaseModel):
    id: MongoObjectId = Field(alias="_id")
    game_num: int
    players: dict[str, MongoObjectId]
    moves: list[str]
    winner: MongoObjectId
