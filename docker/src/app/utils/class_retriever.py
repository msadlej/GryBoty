from src.app.services.file_loader.file_loader import FileLoader
from src.app.services.file_visitor.inheritance_analyzer import InheritanceAnalyzer
import ast


class ClassRetriever:
    def __init__(self, file_str: str):
        self.game_file = file_str
        self.base_classes = {"Game": "Game", "Move": "Move", "Bot": "Bot"}

    def _get_class(self, base_class_key):
        class_name = self.base_classes.get(base_class_key)
        if class_name is None:
            raise ValueError(f"Invalid base class key: {base_class_key}")

        self.analyzer = InheritanceAnalyzer(self.game_file, class_name)
        child_classes = self.analyzer.get_last_children()

        if not child_classes:
            raise ValueError(f"No class inheriting from {class_name} found.")

        return child_classes

    def get_game(self):
        return self._get_class("Game")[0]

    def get_move(self):
        return self._get_class("Move")[0]

    def get_bot(self):
        result = self._get_class("Bot")
        if len(result) > 1:
            raise ValueError("Multiple classes inherit from Bot. Only one is allowed.")
        return result[0]

    def get_method(self, bot_class, method_name):
        body_items = []
        for node in self.analyzer.tree.body:
            if isinstance(node, ast.ClassDef) and node.name == bot_class:
                for body_item in node.body:
                    if (
                        isinstance(body_item, ast.FunctionDef)
                        and body_item.name == method_name
                    ):  # It's a method
                        body_items.append(body_item)
        if len(body_items) > 1:
            raise ValueError(f"Too many methods: {method_name} in {bot_class} class")
        return body_items[0] if len(body_items) > 0 else None
