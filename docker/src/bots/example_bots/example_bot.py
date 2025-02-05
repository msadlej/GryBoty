from two_player_games.move import Move
from two_player_games.player import Player
from two_player_games.state import State


from abc import ABC, abstractmethod


class Bot(Player, ABC):
    @abstractmethod
    def get_move(self, state: State) -> Move:
        raise NotImplementedError
