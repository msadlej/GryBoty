from two_player_games.move import Move
from two_player_games.state import State
from abc import ABC, abstractmethod
from two_player_games.player import Player


class Bot(Player, ABC):
    @abstractmethod
    def get_move(self, state: State) -> Move:
        raise NotImplementedError


class ValidBott(Bot):
    def get_move(self, state: State) -> Move:
        return list(state.get_moves())[0]

    def get_move(self, state: State) -> Move:
        return list(state.get_moves())[1]
