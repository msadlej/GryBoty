from database.main import MongoDB, User, Bot, GameType, Tournament, Match
from datetime import datetime


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
    michal_id = users.create_user(
        "michal",
        "$2b$12$za1Gr8TgVfzzB50wWiVREuiljdBcXeW/90LZuzlWbhbkoOblJ8LNS",
        "standard",
    )
    szlenki_id = users.create_user(
        "szlenki",
        "$2b$12$QbakVoNNX46e93WcZAUPq.MVaT.ec13IcpNR2vE5iS2sd9PWBnZK2",
        "standard",
    )
    users.ban_user(szlenki_id)

    # Add a game to the database
    chess_id = game_types.create_game_type(
        "Chess", "Classical chess game with standard rules"
    )

    # Add bots to the database
    adam_bot_id = bots.create_bot("Chess_Bot_1", chess_id, "chess_bot_code_here")
    jakub_bot_id = bots.create_bot("Chess_Bot_2", chess_id, "chess_bot_code_here")
    users.add_bot(adam_id, adam_bot_id)
    users.add_bot(jakub_id, jakub_bot_id)

    # Add a tournament to the database
    tournament_id = tournaments.create_tournament(
        "Chess Tournament",
        "Description of the tournament",
        chess_id,
        smakuch_id,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "7314",
        16,
    )

    # Add participants to the tournament
    tournaments.add_participant(tournament_id, adam_bot_id)
    tournaments.add_participant(tournament_id, jakub_bot_id)
    match_id = matches.create_match(1, adam_bot_id, jakub_bot_id)
    tournaments.add_match(tournament_id, match_id)

    # Simulate a match
    matches.add_move(match_id, "e2e4")
    matches.add_move(match_id, "e7e5")
    matches.add_move(match_id, "f2f4")
    matches.add_move(match_id, "f7f5")
    matches.set_winner(match_id, adam_bot_id)

    # Update bot stats
    bots.update_stats(adam_bot_id, won=True)
    bots.update_stats(jakub_bot_id, won=False)
