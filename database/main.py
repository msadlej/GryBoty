from typing import List, Dict, Optional
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

class MongoDB:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client.pzsp_database

class User:
    def __init__(self, db: MongoDB):
        self.collection = db.db.users
    
    def create_user(self, username: str, password_hash: str, account_type: str) -> ObjectId:
        user_data = {
            "username": username,
            "password_hash": password_hash,
            "account_type": account_type,
            "bots": [],
            "is_banned": False
        }
        result = self.collection.insert_one(user_data)
        return result.inserted_id
    
    def add_bot(self, user_id: ObjectId, bot_id: ObjectId) -> None:
        self.collection.update_one(
            {"_id": user_id},
            {"$push": {"bots": bot_id}}
        )

    def ban_user(self, user_id: ObjectId) -> None:
        self.collection.update_one(
            {"_id": user_id},
            {"$set": {"is_banned": True}}
        )

class Bot:
    def __init__(self, db: MongoDB):
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
            "tournaments_won": 0
        }
        result = self.collection.insert_one(bot_data)
        return result.inserted_id
    
    def update_stats(self, bot_id: ObjectId, won: bool) -> None:
        update = {
            "$inc": {
                "games_played": 1,
                "wins" if won else "losses": 1
            }
        }
        self.collection.update_one({"_id": bot_id}, update)
    
    def validate_bot(self, bot_id: ObjectId) -> None:
        self.collection.update_one(
            {"_id": bot_id},
            {"$set": {"is_validated": True}}
        )

class GameType:
    def __init__(self, db: MongoDB):
        self.collection = db.db.game_types
    
    def create_game_type(self, name: str, description: str) -> ObjectId:
        game_type_data = {
            "name": name,
            "description": description
        }
        result = self.collection.insert_one(game_type_data)
        return result.inserted_id

class Tournament:
    def __init__(self, db: MongoDB):
        self.collection = db.db.tournaments
    
    def create_tournament(self, name: str, description: str, game_type: ObjectId, creator: ObjectId, start_date: datetime, access_code: str, max_participants: int) -> ObjectId:
        tournament_data = {
            "name": name,
            "description": description,
            "game_type": game_type,
            "creator": creator,
            "start_date": start_date,
            "access_code": access_code,
            "max_participants": max_participants,
            "participants": [],
            "matches": []
        }
        result = self.collection.insert_one(tournament_data)
        return result.inserted_id
    
    def add_participant(self, tournament_id: ObjectId, bot_id: ObjectId) -> bool:
        tournament = self.collection.find_one({"_id": tournament_id})
        if len(tournament["participants"]) < tournament["max_participants"]:
            self.collection.update_one(
                {"_id": tournament_id},
                {"$push": {"participants": bot_id}}
            )
            return True
        return False

class Match:
    def __init__(self, db: MongoDB):
        self.collection = db.db.matches
    
    def create_match(self, game_num: int, bot1_id: ObjectId, bot2_id: ObjectId) -> ObjectId:
        match_data = {
            "game_num": game_num,
            "players": {
                "bot1": bot1_id,
                "bot2": bot2_id
            },
            "moves": [],
            "winner": None
        }
        result = self.collection.insert_one(match_data)
        return result.inserted_id
    
    def add_move(self, match_id: ObjectId, move: str) -> None:
        self.collection.update_one(
            {"_id": match_id},
            {"$push": {"moves": move}}
        )
    
    def set_winner(self, match_id: ObjectId, winner_id: ObjectId) -> None:
        self.collection.update_one(
            {"_id": match_id},
            {"$set": {"winner": winner_id}}
        )
