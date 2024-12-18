from typing import List, Dict, Optional
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId


class MongoDB:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client.pzsp_database

    def get_all_users(self) -> List[Dict]:
        return list(self.db.users.find())

    def get_all_tournaments(self) -> List[Dict]:
        return list(self.db.tournaments.find())

    def get_all_bots(self) -> List[Dict]:
        return list(self.db.bots.find())


class User:
    def __init__(self, db: MongoDB):
        self.db = db.db
        self.collection = db.db.users

    def create_user(
        self, username: str, password_hash: str, account_type: str
    ) -> ObjectId:
        user_data = {
            "username": username,
            "password_hash": password_hash,
            "account_type": account_type,
            "bots": [],
            "is_banned": False,
        }
        result = self.collection.insert_one(user_data)
        return result.inserted_id

    def add_bot(self, user_id: ObjectId, bot_id: ObjectId) -> None:
        self.collection.update_one({"_id": user_id}, {"$push": {"bots": bot_id}})

    def ban_user(self, user_id: ObjectId) -> None:
        self.collection.update_one({"_id": user_id}, {"$set": {"is_banned": True}})

    def get_user_by_id(self, user_id: ObjectId) -> Optional[Dict]:
        return self.collection.find_one({"_id": user_id})

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        return self.collection.find_one({"username": username})

    def get_user_bots(self, user_id: ObjectId) -> List[ObjectId]:
        user = self.get_user_by_id(user_id)
        return user.get("bots", []) if user else []

    def get_all_users(self) -> List[Dict]:
        return list(self.collection.find())


class Bot:
    def __init__(self, db: MongoDB):
        self.db = db.db
        self.collection = db.db.bots

    def create_bot(self, name: str, game_type: ObjectId, code: str) -> ObjectId:
        bot_data = {
            "name": name,
            "game_type": game_type,
            "code": code,
            "is_validated": False,
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "total_tournaments": 0,
            "tournaments_won": 0,
        }
        result = self.collection.insert_one(bot_data)
        return result.inserted_id

    def update_stats(self, bot_id: ObjectId, won: bool) -> None:
        update = {"$inc": {"games_played": 1, "wins" if won else "losses": 1}}
        self.collection.update_one({"_id": bot_id}, update)

    def validate_bot(self, bot_id: ObjectId) -> None:
        self.collection.update_one({"_id": bot_id}, {"$set": {"is_validated": True}})

    def get_bot_by_id(self, bot_id: ObjectId) -> Optional[Dict]:
        return self.collection.find_one({"_id": bot_id})

    def get_bots_by_game_type(self, game_type_id: ObjectId) -> List[Dict]:
        return list(self.collection.find({"game_type": game_type_id}))

    def get_validated_bots(self) -> List[Dict]:
        return list(self.collection.find({"is_validated": True}))

    def get_bot_stats(self, bot_id: ObjectId) -> Optional[Dict]:
        bot = self.get_bot_by_id(bot_id)
        if bot:
            return {
                "games_played": bot.get("games_played", 0),
                "wins": bot.get("wins", 0),
                "losses": bot.get("losses", 0),
                "total_tournaments": bot.get("total_tournaments", 0),
                "tournaments_won": bot.get("tournaments_won", 0),
            }
        return None

    def get_all_bots(self) -> List[Dict]:
        return list(self.collection.find())


class GameType:
    def __init__(self, db: MongoDB):
        self.db = db.db
        self.collection = db.db.game_types

    def create_game_type(self, name: str, description: str) -> ObjectId:
        game_type_data = {"name": name, "description": description}
        result = self.collection.insert_one(game_type_data)
        return result.inserted_id

    def get_game_type_by_id(self, game_type_id: ObjectId) -> Optional[Dict]:
        return self.collection.find_one({"_id": game_type_id})

    def get_game_type_by_name(self, name: str) -> Optional[Dict]:
        return self.collection.find_one({"name": name})

    def get_all_game_types(self) -> List[Dict]:
        return list(self.collection.find())


class Tournament:
    def __init__(self, db: MongoDB):
        self.db = db.db
        self.collection = db.db.tournaments

    def create_tournament(
        self,
        name: str,
        description: str,
        game_type: ObjectId,
        creator: ObjectId,
        start_date: datetime,
        access_code: str,
        max_participants: int,
    ) -> ObjectId:
        tournament_data = {
            "name": name,
            "description": description,
            "game_type": game_type,
            "creator": creator,
            "start_date": start_date,
            "access_code": access_code,
            "max_participants": max_participants,
            "participants": [],
            "matches": [],
        }
        result = self.collection.insert_one(tournament_data)
        return result.inserted_id

    def add_participant(self, tournament_id: ObjectId, bot_id: ObjectId) -> bool:
        tournament = self.collection.find_one({"_id": tournament_id})
        if len(tournament["participants"]) < tournament["max_participants"]:
            self.collection.update_one(
                {"_id": tournament_id}, {"$push": {"participants": bot_id}}
            )
            self.db.bots.update_one({"_id": bot_id}, {"$inc": {"total_tournaments": 1}})

            return True
        return False

    def add_match(self, tournament_id: ObjectId, match_id: ObjectId) -> None:
        self.collection.update_one(
            {"_id": tournament_id}, {"$push": {"matches": match_id}}
        )

    def get_tournament_matches(self, tournament_id: ObjectId) -> List[ObjectId]:
        tournament = self.get_tournament_by_id(tournament_id)
        return tournament.get("matches", []) if tournament else []

    def get_tournament_by_id(self, tournament_id: ObjectId) -> Optional[Dict]:
        return self.collection.find_one({"_id": tournament_id})

    def get_tournaments_by_game_type(self, game_type_id: ObjectId) -> List[Dict]:
        return list(self.collection.find({"game_type": game_type_id}))

    def get_tournaments_by_creator(self, creator_id: ObjectId) -> List[Dict]:
        return list(self.collection.find({"creator": creator_id}))

    def get_tournament_by_match(self, match_id: ObjectId) -> Optional[Dict]:
        return self.collection.find_one({"matches": match_id})

    def get_upcoming_tournaments(self) -> List[Dict]:
        current_date = datetime.now()
        return list(self.collection.find({"start_date": {"$gt": current_date}}))

    def get_tournament_participants(self, tournament_id: ObjectId) -> List[ObjectId]:
        tournament = self.get_tournament_by_id(tournament_id)
        return tournament.get("participants", []) if tournament else []

    def get_tournaments_by_bot_id(self, bot_id: ObjectId) -> List[Dict]:
        return list(self.collection.find({"participants": bot_id}))

    def get_all_tournaments(self) -> List[Dict]:
        return list(self.collection.find())


class Match:
    def __init__(self, db: MongoDB):
        self.db = db.db
        self.collection = db.db.matches

    def create_match(
        self, game_num: int, bot1_id: ObjectId, bot2_id: ObjectId
    ) -> ObjectId:
        match_data = {
            "game_num": game_num,
            "players": {"bot1": bot1_id, "bot2": bot2_id},
            "moves": [],
            "winner": None,
        }
        result = self.collection.insert_one(match_data)
        return result.inserted_id

    def add_move(self, match_id: ObjectId, move: str) -> None:
        self.collection.update_one({"_id": match_id}, {"$push": {"moves": move}})

    def set_winner(self, match_id: ObjectId, winner_id: ObjectId) -> None:
        self.collection.update_one({"_id": match_id}, {"$set": {"winner": winner_id}})

    def get_match_by_id(self, match_id: ObjectId) -> Optional[Dict]:
        return self.collection.find_one({"_id": match_id})

    def get_matches_by_bot(self, bot_id: ObjectId) -> List[Dict]:
        return list(
            self.collection.find(
                {"$or": [{"players.bot1": bot_id}, {"players.bot2": bot_id}]}
            )
        )

    def get_match_moves(self, match_id: ObjectId) -> List[str]:
        match = self.get_match_by_id(match_id)
        return match.get("moves", []) if match else []

    def get_matches_by_winner(self, winner_id: ObjectId) -> List[Dict]:
        return list(self.collection.find({"winner": winner_id}))
