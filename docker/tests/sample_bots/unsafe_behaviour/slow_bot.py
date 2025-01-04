# Import necessary modules
from src.two_player_games.move import Move
from src.two_player_games.state import State
from abc import ABC, abstractmethod
from src.two_player_games.player import Player
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


# Abstract Bot class
class Bot(Player, ABC):
    @abstractmethod
    def get_move(state: State) -> Move:
        """Abstract method to get the next move based on the current state."""
        raise NotImplementedError


# Helper class that performs some operations
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


# Concrete implementation of a Bot that uses various data types and the MoveAnalyzer
class TestBot(Bot):

    def simulate_delay(self, seconds: int) -> None:
        """Simulates a delay for a given number of seconds."""
        end_time = 10**seconds  # Adjusted for a more reasonable delay
        count = 0
        while count < end_time:
            count += 1  # Busy-wait loop to simulate delay

    def get_move(self, state: State) -> Move:

        name = "TestBot"
        history = list("hi")
        settings = dict()
        moves = tuple(["move1", "move2", "move3"])
        available_moves = set(moves)
        counter = 0
        analyzer = MoveAnalyzer()  # Instance of the MoveAnalyzer
        """Returns a random move from the available moves in the current state."""
        self.simulate_delay(1)  # Simulate a delay of 1 second

        # Use some random logic to select a move
        move = random.choice(list(state.get_moves()))
        # print(history)

        for i in range(0, 1):
            i = i + 1
        k = -1
        while k < 0:
            k = k + 1
        # Update history and analyze moves
        history.append(move)
        analyzer.analyze_moves("sth")

        # # Print some debug information
        # print(f"{name} is choosing a move: {move}")
        # print(f"History of moves: {history}")
        # print(f"Current settings: {settings}")
        # print(f"Most common move so far: {analyzer.get_most_common_move()}")
        # result = printed

        return random.choice(list(state.get_moves()))
