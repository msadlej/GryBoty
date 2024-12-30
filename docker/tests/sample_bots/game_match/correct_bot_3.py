from src.bots.example_bots.example_bot import Bot
from src.two_player_games.move import Move
from src.two_player_games.state import State
import random


class ValidBot2(Bot):
    def get_move(self, state: State) -> Move:
        return random.choice(list(state.get_moves()))
