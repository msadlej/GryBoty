from database.main import MongoDB, User, Bot, GameType, Tournament, Match
from datetime import datetime


if __name__ == "__main__":
    db = MongoDB()
    users = User(db)
    bots = Bot(db)
    game_types = GameType(db)
    tournaments = Tournament(db)
    matches = Match(db)

    chess_id = game_types.create_game_type(
        "Chess", "Classical chess game with standard rules"
    )

    user_id1 = users.create_user("standard_user", "hashed_password", "standard")

    user_id2 = users.create_user("premium_user", "hashed_password", "premium")

    bot_id1 = bots.create_bot("Chess_Bot_1", chess_id, "chess_bot_code_here")

    bot_id2 = bots.create_bot("Chess_Bot_2", chess_id, "chess_bot_code_here")

    users.add_bot(user_id1, bot_id1)
    users.add_bot(user_id2, bot_id2)

    tournament_id = tournaments.create_tournament(
        "Chess Tournament",
        "Description of the tournament",
        chess_id,
        user_id2,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "7314",
        16,
    )

    tournaments.add_participant(tournament_id, bot_id1)
    tournaments.add_participant(tournament_id, bot_id2)

    match_id = matches.create_match(1, bot_id1, bot_id2)

    matches.add_move(match_id, "e2e4")
    matches.add_move(match_id, "e7e5")
    matches.add_move(match_id, "f2f4")
    matches.add_move(match_id, "f7f5")

    matches.set_winner(match_id, bot_id1)

    bots.update_stats(bot_id1, won=True)
    bots.update_stats(bot_id2, won=False)
