from src.two_player_games.move import Move
from src.two_player_games.state import State
from abc import ABC, abstractmethod
from src.two_player_games.player import Player
import random


class Bot(Player, ABC):
    @abstractmethod
    def get_move(self, state: State) -> Move:
        raise NotImplementedError


class ValidBot3(Bot):
    def do_sth(self, arg):
        arg + 1

    def get_move(self, state: State) -> Move:
        self.do_sth(1)
        return random.choice(list(state.get_moves()))
