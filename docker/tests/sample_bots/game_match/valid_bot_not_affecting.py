from src.bots.example_bots.example_bot import Bot
from src.two_player_games.move import Move
from src.two_player_games.state import State


class ValidBot3(Bot):
    def get_move(self, state: State) -> Move:
        state._other_player = None
        return list(state.get_moves())[0]
