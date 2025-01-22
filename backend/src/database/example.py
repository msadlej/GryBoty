from datetime import datetime

from database.main import MongoDB, User, Bot, GameType, Tournament, Match


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
    db = MongoDB()
    users = User(db)
    bots = Bot(db)
    game_types = GameType(db)
    tournaments = Tournament(db)
    matches = Match(db)

    # Clear the database
    db.client.drop_database("pzsp_database")

    # Add users to the database
    admin_id = users.create_user(
        "admin",
        "$2b$12$/m9RMY8pH5fGVVUxDHIBAeVzTWPHBkBBYl/QFur9zfKNE/TqWKXgu",
        "admin",
    )
    smakuch_id = users.create_user(
        "smakuch",
        "$2b$12$dTujJVqHwkratt5lpjQcFuitlGA.IIvaMfFRX.OPjNCqwPGgxeN7K",
        "premium",
    )
    adam_id = users.create_user(
        "adam",
        "$2b$12$uuWqsA3vHi0smAk4LDVOS.LJiMfTn1S0Dvp2LPOYF4heiwoNv1xgO",
        "standard",
    )
    jakub_id = users.create_user(
        "jakub",
        "$2b$12$QyMt0LGYTvnM4kYPcGSV5uViMaEW/UvQXAZ5qk0iJn7d9XhxWU5Oq",
        "standard",
    )
    michal_id = users.create_user(
        "michal",
        "$2b$12$za1Gr8TgVfzzB50wWiVREuiljdBcXeW/90LZuzlWbhbkoOblJ8LNS",
        "standard",
    )
    marcin_id = users.create_user(
        "marcin",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    marcin2_id = users.create_user(
        "marcin2",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    marcin3_id = users.create_user(
        "marcin3",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    users.update_ban(marcin_id, True)

    # Add a game to the database
    connect_four_id = game_types.create_game_type(
        "connect_four", "A simple game of Connect Four"
    )

    # Add bots to the database
    adam_bot_id = bots.create_bot("adam_bot", connect_four_id, example_code)
    jakub_bot_id = bots.create_bot("jakub_bot", connect_four_id, example_code)
    michal_bot_id = bots.create_bot("michal_bot", connect_four_id, example_code)
    marcin2_bot_id = bots.create_bot("marcin2_bot", connect_four_id, example_code)
    marcin3_bot_id = bots.create_bot("marcin3_bot", connect_four_id, example_code)
    users.add_bot(adam_id, adam_bot_id)
    users.add_bot(jakub_id, jakub_bot_id)
    users.add_bot(michal_id, michal_bot_id)
    users.add_bot(marcin2_id, marcin2_bot_id)
    users.add_bot(marcin3_id, marcin3_bot_id)
    bots.validate_bot(adam_bot_id)
    bots.validate_bot(jakub_bot_id)
    bots.validate_bot(michal_bot_id)
    bots.validate_bot(marcin2_bot_id)
    bots.validate_bot(marcin3_bot_id)

    # Add a tournament to the database
    connect_four_tournament_id = tournaments.create_tournament(
        "Connect Four Tournament",
        "A tournament of the Connect Four game",
        connect_four_id,
        smakuch_id,
        datetime(2025, 12, 24),
        "REQ2HJ",
        8,
    )

    # Add participants to the tournament
    tournaments.add_participant(connect_four_tournament_id, adam_bot_id)
    tournaments.add_participant(connect_four_tournament_id, jakub_bot_id)
    tournaments.add_participant(connect_four_tournament_id, michal_bot_id)
    tournaments.add_participant(connect_four_tournament_id, marcin2_bot_id)
    tournaments.add_participant(connect_four_tournament_id, marcin3_bot_id)

    # Add example bots to the database
    connect_four_example_bot = bots.create_bot(
        "connect_four_example_bot", connect_four_id, example_code
    )
    users.add_bot(admin_id, connect_four_example_bot)
    bots.validate_bot(connect_four_example_bot)
