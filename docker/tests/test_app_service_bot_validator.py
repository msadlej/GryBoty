import unittest
from unittest.mock import patch
from src.app.services.validation.bot_validation import BotValidationManager


class TestBotGameValidator(unittest.TestCase):
    def test_validate(self):
        bot_path = "docker/src/bots/example_bots/SixMensMorris/bot_1.py"
        game_path = "docker/src/two_player_games/games/morris.py"
        manager = BotValidationManager(bot_path, game_path)
        results = manager.validate()
        print("Validation Results:", results)
        pass


if __name__ == "__main__":
    unittest.main()
