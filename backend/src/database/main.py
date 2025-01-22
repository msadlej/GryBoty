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

    def get_all_game_types(self) -> List[Dict]:
        return list(self.db.game_types.find())


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

    def update_ban(self, user_id: ObjectId, is_banned: bool) -> None:
        self.collection.update_one({"_id": user_id}, {"$set": {"is_banned": is_banned}})

    def update_account_type(self, user_id: ObjectId, new_account_type: str) -> None:
        self.collection.update_one(
            {"_id": user_id}, {"$set": {"account_type": new_account_type}}
        )

    def update_password(self, user_id: ObjectId, new_password_hash: str) -> None:
        self.collection.update_one(
            {"_id": user_id}, {"$set": {"password_hash": new_password_hash}}
        )

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
        self.users_collection = db.db.users

    def create_bot(self, name: str, game_type: ObjectId, code: bytes) -> ObjectId:
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

    def update_name(self, bot_id: ObjectId, new_name: str) -> None:
        self.collection.update_one({"_id": bot_id}, {"$set": {"name": new_name}})

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

    def get_owner(self, bot_id: ObjectId) -> Optional[Dict]:
        return self.users_collection.find_one({"bots": bot_id})

    def delete_bot(self, bot_id: ObjectId) -> bool:
        bot = self.get_bot_by_id(bot_id)
        if not bot:
            return False

        self.users_collection.update_many(
            {"bots": bot_id},
            {"$pull": {"bots": bot_id}}
        )

        tournaments = self.db.tournaments.find({"participants": bot_id})
        for tournament in tournaments:
            if tournament.get("winner") == bot_id:
                self.db.tournaments.update_one(
                    {"_id": tournament["_id"]},
                    {"$set": {"winner": None}}
                )
            self.db.tournaments.update_one(
                {"_id": tournament["_id"]},
                {"$pull": {"participants": bot_id}}
            )

        matches = self.db.matches.find({
            "$or": [
                {"players.0": bot_id},
                {"players.1": bot_id}
            ]
        })

        match_ids = [match["_id"] for match in matches]
        self.db.tournaments.update_many(
            {"matches": {"$in": match_ids}},
            {"$pull": {"matches": {"$in": match_ids}}}
        )

        self.db.matches.delete_many({
            "$or": [
                {"players.0": bot_id},
                {"players.1": bot_id}
            ]
        })

        self.collection.delete_one({"_id": bot_id})

        return True

    def get_tournaments_won(self, bot_id: ObjectId) -> List[Dict]:
        return list(self.db.tournaments.find({"winner": bot_id}))


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
            "winner": None,
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

    def update_name(self, tournament_id: ObjectId, new_name: str) -> None:
        self.collection.update_one({"_id": tournament_id}, {"$set": {"name": new_name}})

    def update_description(self, tournament_id: ObjectId, new_description: str) -> None:
        self.collection.update_one(
            {"_id": tournament_id}, {"$set": {"description": new_description}}
        )

    def update_start_date(
        self, tournament_id: ObjectId, new_start_date: datetime
    ) -> None:
        self.collection.update_one(
            {"_id": tournament_id}, {"$set": {"start_date": new_start_date}}
        )

    def update_max_participants(self, tournament_id: ObjectId, new_max: int) -> bool:
        tournament = self.get_tournament_by_id(tournament_id)
        if len(tournament["participants"]) <= new_max:
            self.collection.update_one(
                {"_id": tournament_id}, {"$set": {"max_participants": new_max}}
            )
            return True
        return False

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

    def get_tournament_by_access_code(self, access_code: str) -> Optional[Dict]:
        return self.collection.find_one({"access_code": access_code})

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

    def set_winner(self, tournament_id: ObjectId, bot_id: ObjectId) -> None:
        self.collection.update_one(
            {"_id": tournament_id},
            {"$set": {"winner": bot_id}}
        )
        self.db.bots.update_one(
            {"_id": bot_id},
            {"$inc": {"tournaments_won": 1}}
        )

    def get_winner(self, tournament_id: ObjectId) -> Optional[ObjectId]:
        tournament = self.get_tournament_by_id(tournament_id)
        return tournament.get("winner") if tournament else None

    def remove_participant(self, tournament_id: ObjectId, bot_id: ObjectId) -> bool:
        tournament = self.collection.find_one({"_id": tournament_id})
        if tournament and bot_id in tournament["participants"]:
            self.collection.update_one(
                {"_id": tournament_id},
                {"$pull": {"participants": bot_id}}
            )
            self.db.bots.update_one(
                {"_id": bot_id},
                {"$inc": {"total_tournaments": -1}}
            )
            return True
        return False


class Match:
    def __init__(self, db: MongoDB):
        self.db = db.db
        self.collection = db.db.matches

    def create_match(
        self, game_num: int, bot1_id: ObjectId, bot2_id: ObjectId
    ) -> ObjectId:
        match_data = {
            "game_num": game_num,
            "players": (bot1_id, bot2_id),
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
                {"$or": [
                    {"players.0": bot_id},
                    {"players.1": bot_id}
                ]}
            )
        )

    def get_match_moves(self, match_id: ObjectId) -> List[str]:
        match = self.get_match_by_id(match_id)
        return match.get("moves", []) if match else []

    def get_matches_by_winner(self, winner_id: ObjectId) -> List[Dict]:
        return list(self.collection.find({"winner": winner_id}))
