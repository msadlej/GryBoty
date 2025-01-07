import unittest
from unittest.mock import patch
import sys
from pathlib import Path
import json
import io

sys.path.append(str(Path(__file__).resolve().parent.parent))


class TestSixMensMorrisBotRun(unittest.TestCase):
    def test_run(self):
        from src.app.services.run_game.bot_runner import BotRunner
        from src.app.services.file_loader.file_loader import FileLoader

        game_name = "morris"

        file_paths = [
            "docker/src/bots/example_bots/testing_bots/bot_1.py",
            "docker/src/bots/example_bots/testing_bots/bot_2.py",
        ]

        file_vars = {}

        for path in file_paths:
            with open(path, "rb") as f:
                file_vars[path] = io.BytesIO(f.read())

        bot_1 = file_vars["docker/src/bots/example_bots/testing_bots/bot_1.py"]
        bot_2 = file_vars["docker/src/bots/example_bots/testing_bots/bot_2.py"]
        bots_map = {bot_1: "bot_1", bot_2: "bot_2"}

        bot_1_str = FileLoader.load_file_as_string(bot_1)
        bot_2_str = FileLoader.load_file_as_string(bot_2)

        runner = BotRunner(game_name, bot_1_str, bot_2_str)
        winner, states = runner.run_game()

        self.assertIn(winner, [bot_1_str, bot_2_str, None])
        self.assertIsInstance(states, list)
        self.assertGreaterEqual(len(states), 0)


if __name__ == "__main__":
    unittest.main()
