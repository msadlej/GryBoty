from src.app.services.validation.validator_base_class import Validator
from src.app.utils.class_retriever import ClassRetriever


class GameMatchingValidator(Validator):
    def __init__(self, bot_path, game_path, bot_class, game_class):
        self.bot_path = bot_path
        self.game_path = game_path
        self.bot_class = bot_class
        self.game_class = game_class

    def validate(self):
        """Validate if the bot matches the game requirements."""
        # game = ClassRetriever(self.game_path)
        retriever = ClassRetriever(self.bot_path)
        bot_classes = retriever.get_bot()
        if len(bot_classes) != 0:
            pass #raise error
        bot_class = bot_classes[0]
        # znajdz ta funkcje i sprawdzy czy ma metode get_move
        print(retriever.has_method(bot_class, 'get_move'))
        # Add logic to check for specific methods, e.g., `get_move`
        return {"game_matching": bot_class}
