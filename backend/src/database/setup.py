from app.utils.database import get_db_connection
from database.main import User, Bot, GameType


example_code = b"""
from src.bots.example_bots.example_bot import Bot
from two_player_games.move import Move
from two_player_games.state import State
import random


class ExampleBot(Bot):
    def get_move(self, state: State) -> Move:
        moves = state.get_moves()
        move = random.choice(moves)
        return move
"""


if __name__ == "__main__":
    with get_db_connection() as db:
        # Clear the database
        db.client.drop_database("gry_boty_database")

        users = User(db)
        bots = Bot(db)
        game_types = GameType(db)

        # Add an admin user to the database
        admin_id = users.create_user(
            "admin",
            "$2b$12$/m9RMY8pH5fGVVUxDHIBAeVzTWPHBkBBYl/QFur9zfKNE/TqWKXgu",
            "admin",
        )

        # Add games to the database
        nim_id = game_types.create_game_type(
            "nim",
            "Nim: A mathematical strategy game where players take turns removing objects from distinct heaps",
        )
        nim_example_bot = bots.create_bot("nim_example_bot", nim_id, example_code)
        users.add_bot(admin_id, nim_example_bot)
        bots.validate_bot(nim_example_bot)
        dots_and_boxes_id = game_types.create_game_type(
            "dots_and_boxes",
            "Dots and Boxes: A strategic paper-and-pencil game where players connect dots to complete squares and claim territory",
        )
        dots_example_bot = bots.create_bot(
            "dots_and_boxes_example_bot", dots_and_boxes_id, example_code
        )
        users.add_bot(admin_id, dots_example_bot)
        bots.validate_bot(dots_example_bot)
        pick_id = game_types.create_game_type(
            "pick",
            "Pick: A mathematical strategy game where players collect numbers to achieve a specific sum",
        )
        pick_example_bot = bots.create_bot("pick_example_bot", pick_id, example_code)
        users.add_bot(admin_id, pick_example_bot)
        bots.validate_bot(pick_example_bot)
        morris_id = game_types.create_game_type(
            "morris",
            "Six Men's Morris: A strategic board game where players place and move pieces to form mills and capture opponents",
        )
        morris_example_bot = bots.create_bot("morris_example_bot", morris_id, example_code)
        users.add_bot(admin_id, morris_example_bot)
        bots.validate_bot(morris_example_bot)
        connect_four_id = game_types.create_game_type(
            "connect_four",
            "Connect Four: A strategic board game where players drop colored tokens to create lines of four in any direction",
        )
        connect_four_example_bot = bots.create_bot(
            "connect_four_example_bot", connect_four_id, example_code
        )
        users.add_bot(admin_id, connect_four_example_bot)
        bots.validate_bot(connect_four_example_bot)
