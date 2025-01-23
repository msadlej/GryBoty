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
