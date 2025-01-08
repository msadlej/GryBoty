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
from src.app.services.validation.runtime_validation import run_with_timer

EXEC_TIME_LIMIT_SEC = 2


class InvalidAttributeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class BotValidationManager(BaseValidator):
    def __init__(self, bot_str, game_name_str):
        super().__init__(bot_str, game_name_str)

    def validate(self):
        """Run all validators and aggregate results."""
        validators = [
            GameMatchingValidatorStatic(
                self.bot_str,
                self.game_name_str,
            ),
            GameValidatorDynamic(self.bot_str, self.game_name_str),
        ]

        for validator in validators:
            validator.validate()
        return True


class GameMatchingValidatorStatic(BaseValidator):
    def __init__(self, bot_str, game_name_str):
        super().__init__(bot_str, game_name_str)

    def validate(self):
        """Validate if the bot matches the game requirements."""
        retriever = ClassRetriever(self.bot_str)
        bot_class = retriever.get_bot()

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
    def __init__(self, bot_str, game_name_str):
        super().__init__(bot_str, game_name_str)
        self.game_move = ClassRetriever(self.game_str).get_move()
        self.move = FileLoader.get_class(self.game_str, self.game_move)
        self.bot_source_code = bot_str

    def validate(self):
        exec_env = self._prepare_execution_environment()
        bot_class = self._load_bot_class(exec_env)
        bot_player, mock_player = self._initialize_players(bot_class)

        self.game = self.game(first_player=bot_player, second_player=mock_player)
        return self._run_game(bot_player)

    def custom_inplacevar(self, op, x, y):
        import operator

        ops = {
            "+=": operator.add,
            "-=": operator.sub,
            "*=": operator.mul,
            "/=": operator.truediv,
            "%=": operator.mod,
        }
        if op in ops:
            return ops[op](x, y)
        raise ValueError(f"Unsupported operation: {op}")

    def _prepare_execution_environment(self):
        restricted_builtins = deepcopy(safe_builtins)
        restricted_builtins.update(
            {
                "__build_class__": __build_class__,
                "__import__": self.restricted_import,
                "_inplacevar_": self.custom_inplacevar,
                "list": list,
                "set": set,
                "tuple": tuple,
                "dict": dict,
                "max": max,
                "min": min,
                "all": all,
                "any": any,
                "filter": filter,
                "range": range,
                "reversed": reversed,
                "sum": sum,
            }
        )

        try:
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
                "_write_": lambda value: value,
            }

            exec(byte_code, exec_env)
            return exec_env
        except SyntaxError as e:
            if 'is an invalid attribute name because it starts with "_"' in str(e):
                raise InvalidAttributeError(f"Invalid attribute name: {e.msg}")
            else:
                raise Exception(e.msg)

    def _load_bot_class(self, exec_env):
        retriever = ClassRetriever(self.bot_str)
        bot_class_name = retriever.get_bot()
        bot_class = FileLoader.get_class(self.bot_str, bot_class_name)
        return exec_env[bot_class.__name__]

    def _initialize_players(self, bot_class):
        bot_player = bot_class(self.game.FIRST_PLAYER_DEFAULT_CHAR)
        mock_player = Bot_1(self.game.SECOND_PLAYER_DEFAULT_CHAR)
        return bot_player, mock_player

    @run_with_timer(max_execution_time=EXEC_TIME_LIMIT_SEC)
    def _run_game(self, bot_player):
        while not self.game.is_finished():
            current_player = self.game.get_current_player()
            state_copy = deepcopy(self.game.state)

            move = current_player.get_move(state_copy)
            if current_player == bot_player:
                self._validate_move_type(move)

            self.game.make_move(move)
            return True

    def _validate_move_type(self, move):
        if not (
            type(move).__name__ == self.move.__name__
            and type(move).__module__ == self.move.__module__
        ):
            raise TypeError(
                f"Invalid move type returned by 'get_move'. Expected {self.move}, got {type(move)}."
            )

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
        if name not in allowed_modules and not name.startswith("two_player_games"):
            raise ImportError(f"Import of '{name}' is not allowed")
        return __import__(name, *args)
