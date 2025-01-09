import unittest
from src.app.services.file_loader.file_loader import FileLoader
import io
from src.app.utils.class_retriever import ClassRetriever


class TestFileLoader(unittest.TestCase):
    def setUp(self):
        game_name = "morris"

        file_paths = [
            "docker/src/bots/example_bots/testing_bots/bot_1.py",
            "docker/src/bots/example_bots/testing_bots/bot_2.py",
        ]

        file_vars = {}

        for path in file_paths:
            with open(path, "rb") as f:
                file_vars[path] = io.BytesIO(f.read())

        bot_1 = file_vars["docker/src/bots/example_bots/testing_bots/bot_1.py"]
        bot_2 = file_vars["docker/src/bots/example_bots/testing_bots/bot_2.py"]

        self.bot_1_file_str = FileLoader.load_file_as_string(bot_1)
        self.bot_2_file_str = FileLoader.load_file_as_string(bot_2)

        self.game_file_str = FileLoader.get_file_str_by_name(game_name)
        self.game_class = ClassRetriever(self.game_file_str).get_game()

        self.bot_1_class = ClassRetriever(self.bot_1_file_str).get_bot()
        self.bot_2_class = ClassRetriever(self.bot_2_file_str).get_bot()

    def test_module_load(self):
        # Test loading modules from strings
        game_module = FileLoader.load_module_from_str(self.game_file_str)
        bot_1_module = FileLoader.load_module_from_str(self.bot_1_file_str)
        bot_2_module = FileLoader.load_module_from_str(self.bot_2_file_str)

        self.assertTrue(hasattr(game_module, "SixMensMorris"))
        self.assertTrue(hasattr(bot_1_module, "Bot_1"))
        self.assertTrue(hasattr(bot_2_module, "Bot_2"))

    def test_retrieve_class(self):
        # Test retrieving classes from loaded modules
        game_module = FileLoader.load_module_from_str(self.game_file_str)
        bot_1_module = FileLoader.load_module_from_str(self.bot_1_file_str)
        bot_2_module = FileLoader.load_module_from_str(self.bot_2_file_str)

        self.assertEqual(
            FileLoader.retrieve_class(bot_1_module, self.bot_1_class).__name__, "Bot_1"
        )
        self.assertEqual(
            FileLoader.retrieve_class(bot_2_module, self.bot_2_class).__name__, "Bot_2"
        )
        self.assertEqual(
            FileLoader.retrieve_class(game_module, self.game_class).__name__,
            "SixMensMorris",
        )

    def test_class_load(self):
        # Test directly loading classes
        self.assertEqual(
            FileLoader.get_class(self.bot_1_file_str, self.bot_1_class).__name__,
            "Bot_1",
        )
        self.assertEqual(
            FileLoader.get_class(self.bot_2_file_str, self.bot_2_class).__name__,
            "Bot_2",
        )
        self.assertEqual(
            FileLoader.get_class(self.game_file_str, self.game_class).__name__,
            "SixMensMorris",
        )

    def test_exceptions(self):
        # Test exceptions for invalid input
        with self.assertRaises(AttributeError):
            fake_module = FileLoader.load_module_from_str(self.bot_1_file_str)
            FileLoader.retrieve_class(fake_module, "NonexistentClass")

        with self.assertRaises(AttributeError):
            FileLoader.get_class(self.bot_1_file_str, "NonexistentClass")

    def test_no_passed_class_attribute_error(self):
        # Test for no matching class in the module
        invalid_module_str = """
class Invalid:
    pass
"""
        with self.assertRaises(
            AttributeError, msg="No matching class found in the module"
        ):
            FileLoader.get_class(invalid_module_str, "SomeClass")
