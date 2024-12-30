from src.app.services.file_loader.file_loader import FileLoader
from src.app.services.validation.bot_game_validator import GameMatchingValidator
from src.app.services.validation.bot_safety_validator import SafetyValidator
from src.app.services.validation.bot_runtime_validator import RuntimeValidator
from src.app.utils.class_retriever import ClassRetriever


class BotValidationManager:
    def __init__(self, bot_path, game_path):
        # TODO: usun nadmiar tych rzeczy tutaj
        self.bot_class = FileLoader.get_class(bot_path)
        self.game_class = ClassRetriever(game_path).get_game()
        self.game = FileLoader.get_class(game_path, self.game_class)
        self.bot_source_code = FileLoader.load_file_as_string(bot_path)
        self.game_source_code = FileLoader.load_file_as_string(game_path)
        self.game_path = game_path
        self.bot_path = bot_path

    def validate(self):
        """Run all validators and aggregate results."""
        validators = [
            SafetyValidator(self.bot_source_code),
            GameMatchingValidator(
                self.bot_path,
                self.game_path,
            ),
            RuntimeValidator(self.bot_class, self.game_class),
        ]

        results = {}
        for validator in validators:
            validator.validate()
        return results


## TODO uruchom jako docker
