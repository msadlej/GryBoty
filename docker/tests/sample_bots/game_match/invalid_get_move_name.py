from src.bots.example_bots.example_bot import Bot
from src.two_player_games.move import Move
from src.two_player_games.state import State
import random


class Bot_1(Bot):
    def get_move(self, stat: State) -> Move:
        moves = stat.get_moves()
        move = random.choice(moves)
        return move
