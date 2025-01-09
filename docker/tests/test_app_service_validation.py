import unittest
from src.app.services.validation.bot_validation import BotValidationManager
from src.app.services.validation.bot_validation import BotValidationManager
from src.app.services.validation.bot_validation import InvalidAttributeError
from src.app.services.validation.runtime_validation import TimeExceededException
from src.app.services.validation.bot_validation import BotValidationManager


class TestGameDynamicBehavior(unittest.TestCase):
    def get_str(self, bot_path):
        # Read the bot file
        with open(bot_path, "r") as f:
            bot_content = f.read()
        return bot_content

    def test_invalid_move_return_type(self):
        bot_str = "docker/tests/sample_bots/game_match/invalid_move_type.py"
        game_str = "nim"

        bot_str = self.get_str(bot_str)

        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_move_return_type_int(self):
        bot_str = "docker/tests/sample_bots/game_match/invalid_move_type_int.py"
        game_str = "nim"

        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_move_return_type_none(self):
        bot_str = "docker/tests/sample_bots/game_match/invalid_move_type_none.py"
        game_str = "nim"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)
        # Perform Validation
        with self.assertRaises(TypeError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Invalid move type returned by 'get_move'.", str(context.exception)
        )

    def test_invalid_remote_access(self):
        bot_str = "docker/tests/sample_bots/unsafe_behaviour/remote_access.py"
        game_str = "nim"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)
        # Perform Validation
        with self.assertRaises(ImportError) as context:
            validator.validate()

        # Assertions
        self.assertIn("Import of 'urllib' is not allowed", str(context.exception))

    def test_invalid_runtime_error(self):
        bot_str = "docker/tests/sample_bots/unsafe_behaviour/runtime_error.py"
        game_str = "nim"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)
        # Perform Validation
        with self.assertRaises(TimeExceededException) as context:
            validator.validate()

        # Assertions
        self.assertIn("Bot does not meet runtime limits.", str(context.exception))

    def test_unauthorized_behavior(self):
        bot_str = "docker/tests/sample_bots/unsafe_behaviour/unauthorized_access.py"
        game_str = "nim"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)
        # Perform Validation
        with self.assertRaises(InvalidAttributeError) as context:
            validator.validate()

        self.assertIn(
            'Invalid attribute name: (\'Line 19: "__dict__" is an invalid attribute name because it starts with "_".\', \'Line 21: "__dict__" is an invalid attribute name because it starts with "_".\')',
            str(context.exception),
        )

    def test_typical(self):
        bot_str = "docker/tests/sample_bots/unsafe_behaviour/typical.py"
        game_str = "nim"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        result = validator.validate()

        self.assertEqual(result, True)

    def test_valid_imports_and_types(self):
        bot_str = "docker/tests/sample_bots/unsafe_behaviour/extended_bot.py"
        game_str = "nim"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)
        # Perform Validation

        result = validator.validate()

        # Assertions
        self.assertEqual(result, True)

    def test_many_get_move(self):
        bot_str = "docker/tests/sample_bots/game_match/bot_2_get_moves.py"
        game_str = "nim"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        with self.assertRaises(ValueError) as context:
            validator.validate()

        self.assertIn(
            "Too many methods: get_move in ValidBott class",
            str(context.exception),
        )


class TestGameMatchingValidator(unittest.TestCase):

    def get_str(self, bot_path):
        with open(bot_path, "r") as f:
            bot_str_content = f.read()
        return bot_str_content

    def test_validate_successful(self):
        bot_str = "docker/tests/sample_bots/game_match/correct_bot.py"
        game_str = "morris"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        result = validator.validate()
        # Assertions
        self.assertEqual(result, True)

    def test_validate_successful_2(self):
        bot_str = "docker/tests/sample_bots/game_match/correct_bot_2.py"
        game_str = "morris"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        result = validator.validate()

        # Assertions
        self.assertEqual(result, True)

    def test_validate_successful_3(self):
        bot_str = "docker/tests/sample_bots/game_match/correct_bot_3.py"
        game_str = "morris"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        result = validator.validate()

        # Assertions
        self.assertEqual(result, True)

    def test_no_bot_class_found(self):
        bot_str = "docker/tests/sample_bots/game_match/no_inheritance.py"
        game_str = "connect_four"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(str(context.exception), "No class inheriting from Bot found.")

    def test_no_bot_class_syntax_error(self):
        bot_str = "docker/tests/sample_bots/game_match/syntax_error.py"
        game_str = "connect_four"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(SyntaxError) as context:
            validator.validate()

        # Assertions

    def test_no_bot_class_found_only_method(self):
        bot_str = "docker/tests/sample_bots/game_match/no_class.py"
        game_str = "connect_four"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(str(context.exception), "No class inheriting from Bot found.")

    def test_no_bot_class_found_empty(self):
        bot_str = "docker/tests/sample_bots/game_match/empty.py"
        game_str = "connect_four"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(str(context.exception), "No class inheriting from Bot found.")

    def test_multiple_bot_classes_found(self):
        bot_str = "docker/tests/sample_bots/game_match/multiple_inheritance.py"
        game_str = "dots_and_boxes"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertEqual(
            str(context.exception),
            "Multiple classes inherit from Bot. Only one is allowed.",
        )

    def test_invalid_get_move_signature_too_many_args(self):
        bot_str = "docker/tests/sample_bots/game_match/invalid_get_move.py"
        game_str = "pick"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "'get_move' method in Bot_1 must accept exactly one argument 'state'.",
            str(context.exception),
        )

    def test_invalid_get_move_signature_wrong_arg_name(self):
        bot_str = "docker/tests/sample_bots/game_match/invalid_get_move_name.py"
        game_str = "pick"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "'get_move' method in Bot_1 must accept exactly one argument 'state'.",
            str(context.exception),
        )

    def test_invalid_get_move_signature_no_get_move(self):
        bot_str = "docker/tests/sample_bots/game_match/no_get_move.py"
        game_str = "pick"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()

        # Assertions
        self.assertIn(
            "Class Bot_1 does not implement 'get_move' method.",
            str(context.exception),
        )

    def test_invalid_get_move_signature_wrong_arg_self(self):
        bot_str = "docker/tests/sample_bots/game_match/invalid_get_move_name_self.py"
        game_str = "pick"
        bot_str = self.get_str(bot_str)
        # Initialize Validator
        validator = BotValidationManager(bot_str, game_str)

        # Perform Validation
        with self.assertRaises(ValueError) as context:
            validator.validate()
        # Assertions
        self.assertIn(
            "'get_move' method in Bot_1 must accept exactly one argument 'state'.",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
