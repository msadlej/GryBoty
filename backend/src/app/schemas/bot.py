from pydantic import BaseModel


class BotModel(BaseModel):
    id: str
    name: str
    game_type: str
    code: str
    is_validated: bool
    games_played: int
    wins: int
    losses: int
    total_tournaments: int
    tournaments_won: int
