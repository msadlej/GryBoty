import sys
import json
from src.app.services.file_loader import FileLoader


class BotRunner:
    def __init__(self, game_path, game_class, bot_1_path, bot_2_path):
        self.game = FileLoader.get_class(game_path, game_class)
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
    game_class = sys.argv[2]
    bot_1 = sys.argv[3]
    bot_2 = sys.argv[4]
    game = BotRunner(game_file, game_class, bot_1, bot_2)
    # TODO: Remove print statement later
    result = game.run_game()
    print(result)
    return result


if __name__ == "__main__":
    main()
