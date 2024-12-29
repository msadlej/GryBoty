import sys
import json
from src.app.services.file_loader.file_loader import FileLoader
from src.app.services.file_visitor.inheritance_analyzer import (
    InheritanceAnalyzer,
)


class BotRunner:
    """
    Initializes and manages a game instance with two competing bots.

    This class dynamically loads the game and bot classes from their respective file paths.
    The game class is selected from the list of derived classes of "Game" (using the first 
    class in the list, assuming it is the intended one). It sets up the game, initializes 
    the bots, and maintains a record of moves and a mapping of bots to their file paths.

    Attributes:
        game_class (list): List of classes derived from "Game" found in the game file.
        game (object): Instance of the selected game class (first in the list).
        bot_1 (object): Instance of the first bot class.
        bot_2 (object): Instance of the second bot class.
        moves (list): List of moves made during the game.
        map (dict): Mapping of bot instances to their file paths.
    """

    def __init__(self, game_path, bot_1_path, bot_2_path):
        self.game_class = InheritanceAnalyzer.get_last_children(
            FileLoader.load_file_as_string(game_path), "Game"
        )
        self.game = FileLoader.get_class(game_path, self.game_class[0])
        self.bot_1 = FileLoader.get_class(bot_1_path)
        self.bot_2 = FileLoader.get_class(bot_2_path)
        self._init_game()
        self.moves = []
        self.map = {self.bot_1: bot_1_path, self.bot_2: bot_2_path}

    def _init_game(self):
        self.bot_1 = self.bot_1(self.game.FIRST_PLAYER_DEFAULT_CHAR)
        self.bot_2 = self.bot_2(self.game.SECOND_PLAYER_DEFAULT_CHAR)
        self.game = self.game(self.bot_1, self.bot_2)

    def run_game(self):
        while not self.game.is_finished():
            current_player = self.game.get_current_player()
            move = current_player.get_move(self.game.state)
            self.moves.append(f"Player {current_player.char}: {str(move)}")
            self.game.make_move(move)

        winner = self.game.get_winner()
        return json.dumps(
            {"winner": self.map.get(winner), "moves": self.moves},
            ensure_ascii=False,
        )


def main():
    game_file = sys.argv[1]
    bot_1 = sys.argv[2]
    bot_2 = sys.argv[3]
    game = BotRunner(game_file, bot_1, bot_2)
    # TODO: Remove print statement later
    result = game.run_game()
    print(result)
    return result


if __name__ == "__main__":
    main()
