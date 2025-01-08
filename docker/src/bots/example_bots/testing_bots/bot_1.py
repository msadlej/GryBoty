from src.bots.example_bots.example_bot import Bot
from two_player_games.move import Move
from two_player_games.state import State
import random


class Bot_1(Bot):
    """
    A simple example implementation of a bot that inherits from the base Bot class.

    This bot randomly selects a move from the available moves in the current game state.

    NOTE:
    - The class name must match the module (file) name, ignoring case. For example,
      if the module is named 'bot_1.py', the class must be named 'Bot_1'.
    - This is a basic bot and should be replaced or extended with more complex logic
      for competitive play.
    - Class must impelment the get_move method
    """

    def get_move(self, state: State) -> Move:
        moves = state.get_moves()
        move = random.choice(moves)
        return move
