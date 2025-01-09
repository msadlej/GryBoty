import inspect
from typing import BinaryIO
import types
import os

# Check if running in Docker (e.g., based on an environment variable)
IN_DOCKER = os.getenv("IN_DOCKER", "false").lower() == "true"

# Adjust base path accordingly
base_path = "" if IN_DOCKER else "docker/"


class FileLoader:
    """
    A utility class to dynamically load modules and retrieve classes from a file.
    """

    @staticmethod
    def get_class(file_str, class_name):
        module = FileLoader.load_module_from_str(file_str)
        return FileLoader.retrieve_class(module, class_name)

    @staticmethod
    def load_module_from_str(file_str):
        module_name = "dynamic_module"
        module = types.ModuleType(module_name)
        exec(file_str, module.__dict__)
        return module

    @staticmethod
    def load_file_as_string(file: BinaryIO):
        return file.getvalue().decode("utf-8")

    @staticmethod
    def retrieve_class(module, class_name=None):
        if class_name is None:
            # Infer class name from file/module name
            classes = inspect.getmembers(
                module,
                lambda member: inspect.isclass(member)
                and member.__module__.lower() == member.__name__.lower(),
            )
            if not classes:
                raise AttributeError("No matching class found in the module.")
            return classes[0][1]
        else:
            if not hasattr(module, class_name):
                raise AttributeError(f"Class '{class_name}' not found in the module.")
            return getattr(module, class_name)

    @staticmethod
    def get_file_str_by_name(game_name: str):
        file_map = {
            "morris": os.path.join(base_path, "two_player_games/games/morris.py"),
            "connect_four": os.path.join(
                base_path, "two_player_games/games/connect_four.py"
            ),
            "dots_and_boxes": os.path.join(
                base_path, "two_player_games/games/dots_and_boxes.py"
            ),
            "nim": os.path.join(base_path, "two_player_games/games/nim.py"),
            "pick": os.path.join(base_path, "two_player_games/games/Pick.py"),
        }

        if game_name not in file_map:
            raise ValueError(f"Game '{game_name}' not found in the file map.")

        with open(file_map[game_name], "r") as f:
            return f.read()
