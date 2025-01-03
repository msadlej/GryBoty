from src.app.services.file_loader.file_loader import FileLoader
from src.app.utils.class_retriever import ClassRetriever
from src.app.services.validation.validator_base_class import BaseValidator
from copy import deepcopy
from src.bots.example_bots.testing_bots.bot_1 import Bot_1

from RestrictedPython import compile_restricted, safe_builtins
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem
from RestrictedPython.Guards import (
    safer_getattr,
    guarded_iter_unpack_sequence,
)
import multiprocessing
from queue import Empty


class BotValidationManager(BaseValidator):
    def __init__(self, bot_path, game_path):
        super().__init__(bot_path, game_path)

    def validate(self):
        """Run all validators and aggregate results."""
        validators = [
            GameMatchingValidatorStatic(
                self.bot_path,
                self.game_path,
            ),
            GameValidatorDynamic(self.bot_path, self.game_path),
        ]

        for validator in validators:
            validator.validate()


class GameMatchingValidatorStatic(BaseValidator):
    def __init__(self, bot_path, game_path):
        super().__init__(bot_path, game_path)

    def validate(self):
        """Validate if the bot matches the game requirements."""
        retriever = ClassRetriever(self.bot_path)
        bot_classes = retriever.get_bot()

        if len(bot_classes) > 1:
            raise ValueError("Multiple classes inherit from Bot. Only one is allowed.")

        bot_class = bot_classes[0]

        func = retriever.get_method(bot_class, "get_move")
        if func is None:
            raise ValueError(f"Class {bot_class} does not implement 'get_move' method.")

        if (
            len(func.args.args) != 2
            or func.args.args[0].arg != "self"
            or func.args.args[1].arg != "state"
        ):
            raise ValueError(
                f"'get_move' method in {bot_class} must accept exactly one argument 'state'."
            )
        return True


class GameValidatorDynamic(BaseValidator):
    def __init__(self, bot_path, game_path, time_limit=2.0):
        super().__init__(bot_path, game_path)
        self.game_move = ClassRetriever(game_path).get_move()
        self.move = FileLoader.get_class(game_path, self.game_move)
        self.time_limit = time_limit
        self.bot_source_code = FileLoader.load_file_as_string(bot_path)

    def validate(self):
        restricted_builtins = deepcopy(safe_builtins)
        restricted_builtins["__build_class__"] = __build_class__
        restricted_builtins["__import__"] = self.restricted_import

        # try:
        byte_code = compile_restricted(
            self.bot_source_code, filename="<bot_code>", mode="exec"
        )
        exec_env = {
            "__builtins__": restricted_builtins,
            "__name__": "restricted_module",
            "__metaclass__": type,
            "_getiter_": default_guarded_getiter,
            "_getitem_": default_guarded_getitem,
            "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
            "_getattr_": safer_getattr,
        }
        exec(byte_code, exec_env)

        retriever = ClassRetriever(self.bot_path)
        bot_classes = retriever.get_bot()
        bot_class = bot_classes[0]
        bot_class = FileLoader.get_class(self.bot_path, bot_class)

        bot_class = exec_env[bot_class.__name__]
        bot_player = bot_class("1")
        mock_player = Bot_1("2")

        self.game = self.game(first_player=bot_player, second_player=mock_player)

        while not self.game.is_finished():
            current_player = self.game.get_current_player()
            state_copy = deepcopy(self.game.state)

            def bot_move(queue, state_copy, current_player):
                try:
                    move = current_player.get_move(state_copy)
                    queue.put(move)
                except Exception as e:
                    queue.put(e)

            queue = multiprocessing.Queue()
            process = multiprocessing.Process(
                target=bot_move, args=(queue, state_copy, current_player)
            )
            process.start()
            process.join(timeout=self.time_limit)

            if process.is_alive():
                process.terminate()
                raise TimeoutError("Bot exceeded time limit for move")

            try:
                result = queue.get_nowait()
                if isinstance(result, Exception):
                    raise result
                move = result
            except Empty:
                raise RuntimeError("Bot does not meet runtime limits.")

            if current_player == bot_player and not (
                type(move).__name__ == self.move.__name__
                and type(move).__module__ == self.move.__module__
            ):
                raise TypeError(
                    f"Invalid move type returned by 'get_move'. Expected {self.move}, got {type(move)}."
                )
            self.game.make_move(move)

    def restricted_import(self, name, *args):
        allowed_modules = {
            "math",
            "random",
            "itertools",
            "functools",
            "collections",
            "numpy",
            "src.bots.example_bots.example_bot",
            "abc",
        }
        if name not in allowed_modules:
            if not name.startswith("src.two_player_games"):
                raise ImportError(f"Import of '{name}' is not allowed")
        return __import__(name, *args)
