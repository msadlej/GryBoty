import importlib.util
import inspect
import os
import sys
import json


class BotRunner:
    def __init__(self, game_path, game_class, bot_1_path, bot_2_path):
        self.game = self.get_class(game_path, game_class)
        self.bot_1 = self.get_class(bot_1_path)
        self.bot_2 = self.get_class(bot_2_path)
        self._init_game()
        self.moves = []
        self.map = {self.bot_1: bot_1_path, self.bot_2: bot_2_path}

    def _init_game(self):
        self.bot_1 = self.bot_1(self.game.FIRST_PLAYER_DEFAULT_CHAR)
        self.bot_2 = self.bot_2(self.game.SECOND_PLAYER_DEFAULT_CHAR)
        self.game = self.game(self.bot_1, self.bot_2)

    def get_class(self, path, class_name=None):
        module = self.load_module(path)
        module_class = self.retrieve_class(module, class_name)
        return module_class

    def load_module(self, path):
        module_name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def retrieve_class(self, module, class_name=None):
        return (
            inspect.getmembers(
                module,
                lambda member: inspect.isclass(member)
                and member.__module__.lower() == member.__name__.lower(),
            )[0][1]
            if class_name is None
            else getattr(module, class_name)
        )

    def run_game(self):
        while not self.game.is_finished():
            current_player = self.game.get_current_player()
            move = current_player.get_move(self.game.state)
            self.moves.append(f"Gracz {current_player.char}: {str(move)}")
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
