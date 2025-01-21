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
    # michal_id = users.create_user(
    #     "michal",
    #     "$2b$12$za1Gr8TgVfzzB50wWiVREuiljdBcXeW/90LZuzlWbhbkoOblJ8LNS",
    #     "standard",
    # )
    marcin_id = users.create_user(
        "marcin",
        "$2b$12$rMRrhTnpEb6kDJZ9nHeWSOVf72WcySUQACT4JHNPI69odwwruHxDa",
        "standard",
    )
    users.update_ban(marcin_id, True)

    # Add a game to the database
    morris_id = game_types.create_game_type("morris", "Six Men's Morris game")
    connect_four_id = game_types.create_game_type(
        "connect_four", "A simple game of Connect Four"
    )

    # Add bots to the database
    adam_bot_id = bots.create_bot("example_bot_1", connect_four_id, example_code)
    jakub_bot_id = bots.create_bot("example_bot_2", connect_four_id, example_code)
    users.add_bot(adam_id, adam_bot_id)
    users.add_bot(jakub_id, jakub_bot_id)
    bots.validate_bot(adam_bot_id)
    bots.validate_bot(jakub_bot_id)

    # Add a tournament to the database
    morris_tournament_id = tournaments.create_tournament(
        "Morris Tournament",
        "A tournament of the Six Men's Morris game",
        morris_id,
        smakuch_id,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "DCIA4N",
        2,
    )
    # connect_four_tournament_id = tournaments.create_tournament(
    #     "Connect Four Tournament",
    #     "A tournament of the Connect Four game",
    #     connect_four_id,
    #     smakuch_id,
    #     datetime.now().strftime("%Y-%m-%d %H:%M"),
    #     "REQ2HJ",
    #     8,
    # )

    # Add participants to the tournament
    tournaments.add_participant(morris_tournament_id, adam_bot_id)
    tournaments.add_participant(morris_tournament_id, jakub_bot_id)
    match_id = matches.create_match(0, adam_bot_id, jakub_bot_id)
    tournaments.add_match(morris_tournament_id, match_id)
