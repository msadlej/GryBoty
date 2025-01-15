from src.app.services.file_loader.file_loader import FileLoader
from src.app.utils.class_retriever import ClassRetriever
from copy import deepcopy


class BotRunner:

    def __init__(
        self, game_name: str, bot_1: str, bot_2: str, bot_1_name: str, bot_2_name: str
    ):
        self._initialize_game(game_name)
        self._initialize_bots(bot_1, bot_2)
        self._init_game()
        self.moves = []
        self.map = {self.bot_1: bot_1_name, self.bot_2: bot_2_name}

    def _initialize_game(self, game_name: str):
        """Load the game file and class."""
        self.game_file_str = FileLoader.get_file_str_by_name(game_name)
        self.game_class = ClassRetriever(self.game_file_str).get_game()
        self.game = FileLoader.get_class(self.game_file_str, self.game_class)

    def _initialize_bots(self, bot_1: str, bot_2: str):
        """Load the bot files and classes."""
        self.bot_class = ClassRetriever(bot_1).get_bot()
        self.bot_class2 = ClassRetriever(bot_2).get_bot()
        self.bot_1 = FileLoader.get_class(bot_1, self.bot_class)
        self.bot_2 = FileLoader.get_class(bot_2, self.bot_class2)

    def _init_game(self):
        self.bot_1 = self.bot_1(self.game.FIRST_PLAYER_DEFAULT_CHAR)
        self.bot_2 = self.bot_2(self.game.SECOND_PLAYER_DEFAULT_CHAR)
        self.game = self.game(first_player=self.bot_1, second_player=self.bot_2)

    def run_game(self):
        while not self.game.is_finished():
            current_player = self.game.get_current_player()
            state_copy = deepcopy(self.game.state)
            move = current_player.get_move(state_copy)
            self.moves.append(str(self.game.state))
            self.game.make_move(move)

        winner = self.game.get_winner()
        winner_str = self.map.get(winner)
        return winner_str, self.moves
