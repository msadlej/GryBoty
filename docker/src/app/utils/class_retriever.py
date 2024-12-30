from src.app.services.file_loader.file_loader import FileLoader
from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer
import ast


class ClassRetriever:
    def __init__(self, game_path):
        self.game_path = game_path
        self.base_classes = {"Game": "Game", "Move": "Move", "Bot": "Bot"}

    def _get_class(self, base_class_key):
        class_name = self.base_classes.get(base_class_key)
        if class_name is None:
            raise ValueError(f"Invalid base class key: {base_class_key}")

        # Load the file content and get the last child class.
        file_content = FileLoader.load_file_as_string(self.game_path)
        self.analyzer = InheritanceAnalyzer(file_content, class_name)
        child_classes = self.analyzer.get_last_children()

        if not child_classes:
            raise ValueError(f"No child classes found for base class {class_name}")

        return child_classes

    def get_game(self):
        return self._get_class("Game")[0]

    def get_move(self):
        return self._get_class("Move")[0]

    def get_bot(self):
        return self._get_class("Bot")

    def has_method(self, bot_class, method_name):
        for node in self.analyzer.tree.body:
            if isinstance(node, ast.ClassDef) and node.name == bot_class:
                for body_item in node.body:
                    if (
                        isinstance(body_item, ast.FunctionDef)
                        and body_item.name == method_name
                    ):  # It's a method
                        return True
        return False
