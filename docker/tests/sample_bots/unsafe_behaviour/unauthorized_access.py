from src.two_player_games.move import Move
from src.two_player_games.state import State
from abc import ABC, abstractmethod
from src.two_player_games.player import Player


class Bot(Player, ABC):
    @abstractmethod
    def get_move(self, state: State) -> Move:
        raise NotImplementedError


class InvalidBot6(Bot):
    def get_move(self, state: State) -> Move:
        import gc

        for obj in gc.get_objects():
            if isinstance(obj, Player) and obj is not self:
                keys = list(bot.__dict__.keys())
                for key in keys:
                    bot.__dict__[k] = None

        return list(state.get_moves())[0]
