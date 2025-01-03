import unittest
from src.app.services.validation.bot_validation import GameValidatorDynamic


class TestGameDynamicBehavior(unittest.TestCase):

    def test_invalid_move_return_type(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_move_type.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_move_return_type_int(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_move_type_int.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_move_return_type_none(self):
        bot_path = "docker/tests/sample_bots/game_match/invalid_move_type_none.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_remote_access(self):
        bot_path = "docker/tests/sample_bots/unsafe_behaviour/remote_access.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(ImportError) as context:
            validator.validate()

        # Assertions
        self.assertIn("Import of 'urllib' is not allowed", str(context.exception))

    def test_invalid_runtime_error(self):
        bot_path = "docker/tests/sample_bots/unsafe_behaviour/runtime_error.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TimeoutError) as context:
            validator.validate()

        # Assertions
        self.assertIn('Bot exceeded time limit for move', str(context.exception))

    def test_unauthorized_behavior(self):
        bot_path = "docker/tests/sample_bots/unsafe_behaviour/unauthorized_access.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(TimeoutError) as context:
            validator.validate()

        # Assertions
        self.assertIn('Bot exceeded time limit for move', str(context.exception))   

        ## restricted python blocks this, handle such syntax error
# InvalidAttributeError(f"Invalid attribute name: \"{key}\" starts with an underscore, which is not allowed. Attribute names should not begin with an underscore.")
# class InvalidAttributeError(Exception):
#     def __init__(self, message):
#         super().__init__(message)