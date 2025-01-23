from datetime import datetime

from database.main import MongoDB, User, Bot, GameType, Tournament, Match
from database.bots import example_code, minimax_code


if __name__ == "__main__":
    db = MongoDB()
    users = User(db)
    bots = Bot(db)
    game_types = GameType(db)
    tournaments = Tournament(db)
    matches = Match(db)

    # Clear the database
    db.client.drop_database("gry_boty_database")

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
    maciej_id = users.create_user(
        "maciej",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    olek_id = users.create_user(
        "olek",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    sebek_id = users.create_user(
        "sebek",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    chad_id = users.create_user(
        "chad",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    users.update_ban(marcin_id, True)

    # Add a game to the database
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

    # Add bots to the database
    adam_bot_id = bots.create_bot("adam_bot", connect_four_id, example_code)
    users.add_bot(adam_id, adam_bot_id)
    bots.validate_bot(adam_bot_id)
    jakub_bot_id = bots.create_bot("jakub_bot", connect_four_id, example_code)
    users.add_bot(jakub_id, jakub_bot_id)
    bots.validate_bot(jakub_bot_id)
    michal_bot_id = bots.create_bot("michal_bot", connect_four_id, example_code)
    users.add_bot(michal_id, michal_bot_id)
    bots.validate_bot(michal_bot_id)
    maciej_bot_id = bots.create_bot("maciej_bot", connect_four_id, example_code)
    users.add_bot(maciej_id, maciej_bot_id)
    bots.validate_bot(maciej_bot_id)
    olek_bot_id = bots.create_bot("olek_bot", connect_four_id, example_code)
    users.add_bot(olek_id, olek_bot_id)
    bots.validate_bot(olek_bot_id)
    sebek_bot_id = bots.create_bot("sebek_bot", connect_four_id, example_code)
    users.add_bot(sebek_id, sebek_bot_id)
    bots.validate_bot(sebek_bot_id)
    chad_bot_id = bots.create_bot("chad_bot", connect_four_id, minimax_code)
    users.add_bot(chad_id, chad_bot_id)
    bots.validate_bot(chad_bot_id)

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
    tournaments.add_participant(connect_four_tournament_id, maciej_bot_id)
    tournaments.add_participant(connect_four_tournament_id, olek_bot_id)
    tournaments.add_participant(connect_four_tournament_id, sebek_bot_id)
    tournaments.add_participant(connect_four_tournament_id, chad_bot_id)
