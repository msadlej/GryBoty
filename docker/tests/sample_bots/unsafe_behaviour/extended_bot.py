# Import necessary modules
from two_player_games.move import Move
from two_player_games.state import State
from abc import ABC, abstractmethod
from two_player_games.player import Player
import random
import math
import itertools
import functools
import collections
import numpy as np

# Define the allowed modules
allowed_modules = {
    "math",
    "random",
    "itertools",
    "functools",
    "collections",
    "numpy",
    "src.bots.example_bots.example_bot",
    "abc",
}


class Bot(Player, ABC):
    @abstractmethod
    def get_move(state: State) -> Move:
        """Abstract method to get the next move based on the current state."""
        raise NotImplementedError


class MoveAnalyzer:
    def __init__(self):
        self.move_statistics = collections.defaultdict(int)

    def analyze_moves(self, moves: list) -> dict:
        """Analyze the moves and return statistics."""
        for move in moves:
            self.move_statistics[move] = self.move_statistics.get(move, 0) + 1
        return dict(self.move_statistics)

    def get_most_common_move(self) -> str:
        """Return the most common move."""
        if not self.move_statistics:
            return None
        return max(self.move_statistics.items(), key=lambda x: x[1])[0]


class TestBot(Bot):

    def simulate_delay(self, seconds: int) -> None:
        """Simulates a delay for a given number of seconds."""
        end_time = 10 * seconds
        count = 0
        while count < end_time:
            count += 1

    def get_move(self, state: State) -> Move:

        name = "TestBot"
        history = list("hi")
        settings = dict()
        moves = tuple(["move1", "move2", "move3"])
        available_moves = set(moves)
        counter = 0
        analyzer = MoveAnalyzer()

        self.simulate_delay(1)

        move = random.choice(list(state.get_moves()))

        for i in range(0, 1):
            i = i + 1
        k = -1

        while k < 0:
            k = k + 1

        p = [j for j in range(2)]

        history.append(move)
        analyzer.analyze_moves("sthh")
        analyzer.get_most_common_move()

        return random.choice(list(state.get_moves()))
