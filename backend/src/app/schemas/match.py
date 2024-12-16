from pydantic import BaseModel


class MatchModel(BaseModel):
    id: str
    game_num: int
    players: dict[str, str]
    moves: list[str]
    winner: str
