from src.app.services.validation.validator_base_class import Validator
from src.app.utils.class_retriever import ClassRetriever
from src.app.services.file_loader.file_loader import FileLoader
from src.two_player_games.player import Player


class GameMatchingValidator(Validator):
    def __init__(self, bot_path, game_path):
        self.game_class = ClassRetriever(game_path).get_game()
        self.game = FileLoader.get_class(game_path, self.game_class)
        self.bot_path = bot_path
        self.game_path = game_path
        self.game_move = ClassRetriever(game_path).get_move()
        self.move = FileLoader.get_class(game_path, self.game_move)
        pass

    def validate(self):
        """Validate if the bot matches the game requirements."""
        retriever = ClassRetriever(self.bot_path)
        bot_classes = retriever.get_bot()

        if len(bot_classes) > 1:
            raise ValueError("Multiple classes inherit from Bot. Only one is allowed.")

        bot_class = bot_classes[0]

        # Validate the get_move method
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

        # Instantiate bot and players
        bot_instance = FileLoader.get_class(self.bot_path, bot_class)
        bot_player = bot_instance("1")
        mock_player = Player("2")

        # Initialize the game
        self.game = self.game(first_player=bot_player, second_player=mock_player)

        # Test the bot's move
        move = bot_player.get_move(self.game.state)
        if not (
            type(move).__name__ == self.move.__name__
            and type(move).__module__ == self.move.__module__
        ):
            raise TypeError(
                f"Invalid move type returned by 'get_move'. Expected {self.move}, got {type(move)}."
            )

        # Return validation result
        return True
