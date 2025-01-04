import unittest
from src.app.services.validation.bot_validation import GameValidatorDynamic
from src.app.services.validation.bot_validation import InvalidAttributeError
from src.app.services.validation.runtime_validation import TimeExceededException


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
        with self.assertRaises(TimeExceededException) as context:
            validator.validate()

        # Assertions
        self.assertIn("Bot does not meet runtime limits.", str(context.exception))

    def test_unauthorized_behavior(self):
        bot_path = "docker/tests/sample_bots/unsafe_behaviour/unauthorized_access.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation
        with self.assertRaises(InvalidAttributeError) as context:
            validator.validate()

        self.assertIn(
            'Invalid attribute name: (\'Line 19: "__dict__" is an invalid attribute name because it starts with "_".\', \'Line 21: "__dict__" is an invalid attribute name because it starts with "_".\')',
            str(context.exception),
        )

    def test_typical(self):
        bot_path = "docker/tests/sample_bots/unsafe_behaviour/typical.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)

        result = validator.validate()

        self.assertEqual(result, True)

    def test_valid_imports_and_types(self):
        bot_path = "docker/tests/sample_bots/unsafe_behaviour/slow_bot.py"
        game_path = "docker/src/two_player_games/games/Pick.py"

        # Initialize Validator
        validator = GameValidatorDynamic(bot_path, game_path)
        # Perform Validation

        result = validator.validate()

        # Assertions
        self.assertEqual(result, True)


# TODO: zmien nazwe bota
# zapisz sobie czego nie mozna: self, +=1, inita, taki poradnik dla uzytkownika
# usun printa 
# zmien testy zamiast sciezki, string? docker
# napisz jeszcze kilka botow dla pewnosci
# polacz testy walidacji bota w jeden plik, nie ma sensu rozdzielac
