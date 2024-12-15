from app.schemas.tournament import TournamentModel
from database.main import MongoDB, Tournament
from app.schemas.user import UserModel
from bson import ObjectId


def get_tournaments_by_creator(creator: UserModel) -> list[TournamentModel] | None:
    db = MongoDB()
    tournaments = Tournament(db)
    tournaments_by_creator = tournaments.get_tournaments_by_creator(
        ObjectId(creator.id)
    )

    if not tournaments_by_creator:
        return None

    return [
        TournamentModel(
            id=str(tournament["_id"]),
            name=str(tournament["name"]),
            description=str(tournament["description"]),
            game_type=str(tournament["game_type"]),
            creator=str(tournament["creator"]),
            start_date=str(tournament["start_date"]),
            access_code=str(tournament["access_code"]),
            max_participants=tournament["max_participants"],
            participants=[
                str(participant) for participant in tournament["participants"]
            ],
            matches=[str(match) for match in tournament["matches"]],
        )
        for tournament in tournaments_by_creator
    ]
