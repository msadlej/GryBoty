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

minimax_code = b"""
from src.bots.example_bots.example_bot import Bot
from two_player_games.move import Move
from two_player_games.state import State
from two_player_games.state import Player
from typing import Optional, List, Dict, Tuple


class Heuristic:
    def get_heuristic(self, state: State) -> int:
        player_values = {"max": 0, "min": 0}
        self.state = state
        fields = self.state.fields[1:]
        self.evaluate_lines(fields, player_values)
        return self.final_heuristic(player_values)

    def evaluate_lines(
        self, fields: List[List[Player]], player_values: Dict[str, int]
    ) -> None:
        directions = [
            ((0, 1), self.get_number_vertical),
            ((1, 0), self.get_number_horizontal),
            ((1, 1), self.get_number_desc_diagonals),
            ((1, -1), self.get_number_asc_diagonals),
        ]

        for direction, method in directions:
            method(fields, player_values, direction)

    def get_number_in_line(
        self,
        start_coords: Tuple[int, int],
        move_coords: Tuple[int, int],
        fields: List[List[Player]],
    ) -> Optional[Dict[str, int]]:
        field = {}
        for i in range(4):
            player = fields[start_coords[0] + move_coords[0] * i][
                start_coords[1] + move_coords[1] * i
            ]
            if player:
                field[player] = field.get(player, 0) + 1
        return field if len(field) == 1 else None

    def update_player_values(
        self, player_score: Dict[str, int], player_values: Dict[str, int]
    ) -> None:
        if player_score:
            player, count = next(iter(player_score.items()))
            value = self.calculate_heuristics(count)
            player_values[
                "max" if player == self.state.get_current_player() else "min"
            ] = (
                player_values[
                    "max" if player == self.state.get_current_player() else "min"
                ]
                + value
            )

    def get_number_vertical(
        self,
        fields: List[List[Player]],
        player_values: Dict[str, int],
        direction: Tuple[int, int],
    ) -> None:
        for column in range(len(fields)):
            for row in range(len(fields[column]) - 3):
                score = self.get_number_in_line((column, row), direction, fields)
                if score:
                    self.update_player_values(score, player_values)

    def get_number_horizontal(
        self,
        fields: List[List[Player]],
        player_values: Dict[str, int],
        direction: Tuple[int, int],
    ) -> None:
        for row in range(len(fields)):
            for col in range(len(fields) - 3):
                score = self.get_number_in_line((col, row), direction, fields)
                if score:
                    self.update_player_values(score, player_values)

    def get_number_desc_diagonals(
        self,
        fields: List[List[Player]],
        player_values: Dict[str, int],
        direction: Tuple[int, int],
    ) -> None:
        for col in range(len(fields) - 3):
            for row in range(len(fields[col]) - 3):
                score = self.get_number_in_line((col, row), direction, fields)
                if score:
                    self.update_player_values(score, player_values)

    def get_number_asc_diagonals(
        self,
        fields: List[List[Player]],
        player_values: Dict[str, int],
        direction: Tuple[int, int],
    ) -> None:
        for col in range(len(fields) - 3):
            for row in range(3, len(fields[col])):
                score = self.get_number_in_line((col, row), direction, fields)
                if score:
                    self.update_player_values(score, player_values)

    def calculate_heuristics(self, number_in_line: int) -> int:
        heuristics = {2: 2, 3: 5, 4: 100}
        return heuristics.get(number_in_line, 0)

    def final_heuristic(self, player_values: Dict[str, int]) -> int:
        return player_values["max"] - player_values["min"]


class MiniMax:
    def __init__(self, depth_limit: int):
        self.depth_limit = depth_limit

    def get_best_move(self, state: State, is_maximizing_player: bool) -> Move:
        best_value = float("-inf") if is_maximizing_player else float("inf")
        best_move = None

        for move in state.get_moves():
            new_state = state.make_move(move)
            value = self.minimax(
                new_state,
                self.depth_limit - 1,
                not is_maximizing_player,
                float("-inf"),
                float("inf"),
            )

            if (is_maximizing_player and value > best_value) or (
                not is_maximizing_player and value < best_value
            ):
                best_value = value
                best_move = move

        return best_move

    def minimax(
        self,
        state: State,
        depth: int,
        is_maximizing_player: bool,
        alpha: float,
        beta: float,
    ) -> float:
        if depth == 0 or state.is_finished():
            return Heuristic().get_heuristic(state)

        if is_maximizing_player:
            max_eval = float("-inf")
            for move in state.get_moves():
                new_state = state.make_move(move)
                eval = self.minimax(new_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in state.get_moves():
                new_state = state.make_move(move)
                eval = self.minimax(new_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


class MyBot(Bot):
    minimax = MiniMax(depth_limit=3)

    def get_move(self, state: State) -> Move:
        return self.minimax.get_best_move(state, is_maximizing_player=True)
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
    connect_four_id = game_types.create_game_type(
        "connect_four", "A simple game of Connect Four"
    )

    # Add bots to the database
    adam_bot_id = bots.create_bot("adam_bot", connect_four_id, example_code)
    jakub_bot_id = bots.create_bot("jakub_bot", connect_four_id, example_code)
    michal_bot_id = bots.create_bot("michal_bot", connect_four_id, example_code)
    maciej_bot_id = bots.create_bot("maciej_bot", connect_four_id, example_code)
    olek_bot_id = bots.create_bot("olek_bot", connect_four_id, example_code)
    sebek_bot_id = bots.create_bot("sebek_bot", connect_four_id, example_code)
    chad_bot_id = bots.create_bot("chad_bot", connect_four_id, minimax_code)
    users.add_bot(adam_id, adam_bot_id)
    users.add_bot(jakub_id, jakub_bot_id)
    users.add_bot(michal_id, michal_bot_id)
    users.add_bot(maciej_id, maciej_bot_id)
    users.add_bot(olek_id, olek_bot_id)
    users.add_bot(sebek_id, sebek_bot_id)
    users.add_bot(chad_id, chad_bot_id)
    bots.validate_bot(adam_bot_id)
    bots.validate_bot(jakub_bot_id)
    bots.validate_bot(michal_bot_id)
    bots.validate_bot(maciej_bot_id)
    bots.validate_bot(olek_bot_id)
    bots.validate_bot(sebek_bot_id)
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

    # Add example bots to the database
    connect_four_example_bot = bots.create_bot(
        "connect_four_example_bot", connect_four_id, example_code
    )
    users.add_bot(admin_id, connect_four_example_bot)
    bots.validate_bot(connect_four_example_bot)
