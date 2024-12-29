import unittest
from unittest.mock import patch
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).resolve().parent.parent))


class TestSixMensMorrisBotRun(unittest.TestCase):

    @patch(
        "sys.argv",
        [
            "docker/app/services/bot_runner.py",
            "docker/src/two_player_games/games/morris.py",
            "docker/src/bots/example_bots/SixMensMorris/bot_1.py",
            "docker/src/bots/example_bots/SixMensMorris/bot_2.py",
        ],
    )
    def test_run(self):
        from src.app.services.run_game.bot_runner import main

        result = main()
        self.assertIsInstance(result, str)
        result_dict = json.loads(result)
        self.assertEqual(len(result_dict.keys()), 2)
        self.assertIn("winner", result_dict)
        self.assertIn("moves", result_dict)
        self.assertIn(result_dict["winner"], [sys.argv[2], sys.argv[3], None])
        self.assertIsInstance(result_dict["moves"], list)
        self.assertGreaterEqual(len(result_dict["moves"]), 0)


if __name__ == "__main__":
    unittest.main()
