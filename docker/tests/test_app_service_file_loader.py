import unittest
from unittest.mock import patch
from src.app.services.file_loader import FileLoader
from src.bots.example_bots.SixMensMorris.bot_1 import Bot_1
from src.bots.example_bots.SixMensMorris.bot_2 import Bot_2
from src.two_player_games.games.morris import SixMensMorris
import sys
import os


class TestFileLoader(unittest.TestCase):
    @patch(
        "sys.argv",
        [
            "docker/src/two_player_games/games/morris.py",
            "SixMensMorris",
            "docker/src/bots/example_bots/SixMensMorris/bot_1.py",
            "docker/src/bots/example_bots/SixMensMorris/bot_2.py",
        ],
    )
    def setUp(self):
        self.game_file = sys.argv[0]
        self.game_class = sys.argv[1]
        self.bot_1_file = sys.argv[2]
        self.bot_2_file = sys.argv[3]

    def _load_and_assert_module(self, file_path, expected_name):
        module = FileLoader.load_module(file_path)
        self.assertEqual(module.__name__, expected_name)
        return module

    def test_module_load(self):
        self._load_and_assert_module(self.bot_1_file, "bot_1")
        self._load_and_assert_module(self.bot_2_file, "bot_2")
        self._load_and_assert_module(self.game_file, "morris")

    def test_retrieve_class(self):
        bot_1_module = self._load_and_assert_module(self.bot_1_file, "bot_1")
        bot_2_module = self._load_and_assert_module(self.bot_2_file, "bot_2")
        game_module = self._load_and_assert_module(self.game_file, "morris")
        self.assertEqual(
            FileLoader.retrieve_class(bot_1_module).__name__, Bot_1.__name__
        )
        self.assertEqual(
            FileLoader.retrieve_class(bot_2_module).__name__, Bot_2.__name__
        )
        self.assertEqual(
            FileLoader.retrieve_class(game_module, self.game_class).__name__,
            SixMensMorris.__name__,
        )

    def test_class_load(self):
        self.assertEqual(FileLoader.get_class(self.bot_1_file).__name__, Bot_1.__name__)
        self.assertEqual(FileLoader.get_class(self.bot_2_file).__name__, Bot_2.__name__)
        self.assertEqual(
            FileLoader.get_class(self.game_file, self.game_class).__name__,
            SixMensMorris.__name__,
        )

    def test_exceptions(self):
        with self.assertRaises(FileNotFoundError):
            FileLoader.load_module("nonexistent_file.py")

        with self.assertRaises(FileNotFoundError):
            FileLoader.load_module("/invalid/path/to/module.py")

        with self.assertRaises(AttributeError):
            fake_module = self._load_and_assert_module(self.bot_1_file, "bot_1")
            FileLoader.retrieve_class(fake_module, "NonexistentClass")

        with self.assertRaises(AttributeError):
            FileLoader.get_class(self.bot_1_file, "NonexistentClass")

    def test_no_passed_class_attribute_error(self):
        import tempfile

        with tempfile.NamedTemporaryFile(
            suffix=".py", prefix="test", delete=False
        ) as tmp_file:
            tmp_file.write(b"class Invalid:\n pass")  # Write invalid Python code

        try:
            with self.assertRaises(
                AttributeError, msg="No matching class found in the module"
            ):
                FileLoader.get_class(tmp_file.name)
        finally:
            os.remove(tmp_file.name)  # Clean up the temporary file
