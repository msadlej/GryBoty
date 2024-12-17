import unittest
from unittest.mock import patch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


class TestSixMensMorrisBotRun(unittest.TestCase):

    @patch(
        "sys.argv",
        [
            "src/app/services/bot_runner.py",
            "src/two_player_games/games/morris.py",
            "SixMensMorris",
            "src/bots/example_bots/SixMensMorris/bot_1.py",
            "src/bots/example_bots/SixMensMorris/bot_2.py",
        ],
    )
    def test_run(self):
        from src.app.services.bot_runner import main

        result = main()
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0] in [sys.argv[3], sys.argv[4], None])
        self.assertEqual(len(result[1].keys()), 2)

        self.assertIn(sys.argv[3], result[1])
        self.assertIn(sys.argv[4], result[1])


class TestBotRunner(unittest.TestCase):
    @patch(
        "sys.argv",
        [
            "src/app/services/bot_runner.py",
            "src/two_player_games/games/morris.py",
            "SixMensMorris",
            "src/bots/example_bots/SixMensMorris/bot_1.py",
            "src/bots/example_bots/SixMensMorris/bot_2.py",
        ],
    )
    def test_module_load(self):
        from src.app.services.bot_runner import BotRunner

        game_file = sys.argv[1]
        game_class = sys.argv[2]
        bot_1 = sys.argv[3]
        bot_2 = sys.argv[4]
        bot_runner = BotRunner(game_file, game_class, bot_1, bot_2)
        self.assertEqual(bot_runner.load_module(bot_1).__name__, "bot_1")
        self.assertEqual(bot_runner.load_module(bot_2).__name__, "bot_2")
        self.assertEqual(bot_runner.load_module(game_file).__name__, "morris")

    @patch(
        "sys.argv",
        [
            "src/app/services/bot_runner.py",
            "src/two_player_games/games/morris.py",
            "SixMensMorris",
            "src/bots/example_bots/SixMensMorris/bot_1.py",
            "src/bots/example_bots/SixMensMorris/bot_2.py",
        ],
    )
    def test_retrieve_class(self):
        from src.app.services.bot_runner import BotRunner
        from src.bots.example_bots.SixMensMorris.bot_1 import Bot_1
        from src.bots.example_bots.SixMensMorris.bot_2 import Bot_2
        from src.two_player_games.games.morris import SixMensMorris

        game_file = sys.argv[1]
        game_class = sys.argv[2]
        bot_1 = sys.argv[3]
        bot_2 = sys.argv[4]
        bot_runner = BotRunner(game_file, game_class, bot_1, bot_2)
        bot_1_module = bot_runner.load_module(bot_1)
        bot_2_module = bot_runner.load_module(bot_2)
        game_module = bot_runner.load_module(game_file)
        self.assertEqual(
            bot_runner.retrieve_class(bot_1_module).__name__, Bot_1.__name__
        )
        self.assertEqual(
            bot_runner.retrieve_class(bot_2_module).__name__, Bot_2.__name__
        )
        self.assertEqual(
            bot_runner.retrieve_class(game_module, game_class).__name__,
            SixMensMorris.__name__,
        )

    @patch(
        "sys.argv",
        [
            "src/app/services/bot_runner.py",
            "src/two_player_games/games/morris.py",
            "SixMensMorris",
            "src/bots/example_bots/SixMensMorris/bot_1.py",
            "src/bots/example_bots/SixMensMorris/bot_2.py",
        ],
    )
    def test_class_load(self):
        from src.app.services.bot_runner import BotRunner
        from src.bots.example_bots.SixMensMorris.bot_1 import Bot_1
        from src.bots.example_bots.SixMensMorris.bot_2 import Bot_2
        from src.two_player_games.games.morris import SixMensMorris

        game_file = sys.argv[1]
        game_class = sys.argv[2]
        bot_1 = sys.argv[3]
        bot_2 = sys.argv[4]
        bot_runner = BotRunner(game_file, game_class, bot_1, bot_2)
        self.assertEqual(bot_runner.get_class(bot_1).__name__, Bot_1.__name__)
        self.assertEqual(bot_runner.get_class(bot_2).__name__, Bot_2.__name__)
        self.assertEqual(
            bot_runner.get_class(game_file, game_class).__name__,
            SixMensMorris.__name__,
        )


# class TestConnectFourBotRun(unittest.TestCase):
#     @patch(
#         "sys.argv",
#         [
#             "src/app/services/bot_runner.py",
#             "src/two_player_games/games/morris.py",
#             "SixMensMorris",
#             "src/bots/example_bots/SixMensMorris/bot_1.py",
#             "src/bots/example_bots/SixMensMorris/bot_2.py",
#         ],
#     )
#     def test_run(self):
#         result = main()
#         self.assertEqual(len(result), 2)
#         self.assertTrue(result[0] in [sys.argv[3], sys.argv[4], None])


# class TestDotsAndBoxesBotRun(unittest.TestCase):
#     @patch(
#         "sys.argv",
#         [
#             "src/app/services/bot_runner.py",
#             "src/two_player_games/games/morris.py",
#             "SixMensMorris",
#             "src/bots/example_bots/SixMensMorris/bot_1.py",
#             "src/bots/example_bots/SixMensMorris/bot_2.py",
#         ],
#     )
#     def test_run(self):
#         result = main()
#         self.assertEqual(len(result), 2)
#         self.assertTrue(result[0] in [sys.argv[3], sys.argv[4], None])


# class TestNimBotRun(unittest.TestCase):
#     @patch(
#         "sys.argv",
#         [
#             "src/app/services/bot_runner.py",
#             "src/two_player_games/games/morris.py",
#             "SixMensMorris",
#             "src/bots/example_bots/SixMensMorris/bot_1.py",
#             "src/bots/example_bots/SixMensMorris/bot_2.py",
#         ],
#     )
#     def test_run(self):
#         result = main()
#         self.assertEqual(len(result), 2)
#         self.assertTrue(result[0] in [sys.argv[3], sys.argv[4], None])


# class TestPickBotRun(unittest.TestCase):
#     @patch(
#         "sys.argv",
#         [
#             "src/app/services/bot_runner.py",
#             "src/two_player_games/games/morris.py",
#             "SixMensMorris",
#             "src/bots/example_bots/SixMensMorris/bot_1.py",
#             "src/bots/example_bots/SixMensMorris/bot_2.py",
#         ],
#     )
#     def test_run(self):
#         result = main()
#         self.assertEqual(len(result), 2)
#         self.assertTrue(result[0] in [sys.argv[3], sys.argv[4], None])


if __name__ == "__main__":
    unittest.main()
