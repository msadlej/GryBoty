from src.app.services.file_loader.file_loader import FileLoader
from src.app.utils.class_retriever import ClassRetriever


class BaseValidator:
    def __init__(self, bot_path, game_path):
        self.bot_path = bot_path
        self.game_path = game_path
        self.game_class = ClassRetriever(game_path).get_game()
        self.game = FileLoader.get_class(game_path, self.game_class)