from pydantic import BaseModel


class TournamentModel(BaseModel):
    id: str
    name: str
    description: str
    game_type: str
    creator: str
    start_date: str
    access_code: str
    max_participants: int
    participants: list[str]
    matches: list[str]
