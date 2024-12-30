from src.app.services.validation.validator_base_class import Validator


class RuntimeValidator(Validator):
    def __init__(self, bot_class, game_class):
        self.bot_class = bot_class
        self.game_class = game_class

    def validate(self):
        """Run the bot and validate its execution time and stability."""
        # Mock implementation for runtime validation
        return {"runtime": "no_errors"}
