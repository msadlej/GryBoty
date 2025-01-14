from src.app.services.file_loader.file_loader import FileLoader
from src.app.utils.class_retriever import ClassRetriever


class BaseValidator:
    def __init__(self, bot_str, game_name_str):
        self.bot_str = bot_str
        self.game_name_str = game_name_str
        self.game_str = FileLoader.get_file_str_by_name(game_name_str)
        self.game_class = ClassRetriever(self.game_str).get_game()
        self.game = FileLoader.get_class(self.game_str, self.game_class)
