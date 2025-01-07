from src.app.services.file_loader.file_loader import FileLoader
from src.app.utils.class_retriever import ClassRetriever


class BaseValidator:
    def __init__(self, bot_str, game_str):
        self.bot_str = bot_str
        self.game_str = game_str
        self.game_class = ClassRetriever(game_str).get_game()
        self.game = FileLoader.get_class(game_str, self.game_class)
