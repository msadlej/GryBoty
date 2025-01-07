import unittest
from fastapi.testclient import TestClient
from main import app  # Replace with your actual app module
from io import BytesIO

client = TestClient(app)


class TestRunMatch(unittest.TestCase):
    def test_run_match_no_bot_class(self):
        game_name = "morris"
        bot1_content = "print('Bot 1 logic')"
        bot2_content = "print('Bot 2 logic')"
        filename1 = "bot1.py"
        filename2 = "bot2.py"

        response = client.post(
            "/run-match",
            data={
                "game": game_name,
                "file1": bot1_content.encode(),
                "file2": bot2_content.encode(),
                "filename1": filename1,
                "filename2": filename2,
            },
        )

        assert response.status_code != 200
        data = response.json()
        print(data["detail"])
        assert data["detail"] == "No class inheriting from Bot found."

    def test_typical_valid(self):
        game_name = "dots_and_boxes"
        bot1_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"
        bot2_path = "docker/src/bots/example_bots/testing_bots/bot_2.py"

        with open(bot1_path, "rb") as f:
            bot1_content = f.read()

        with open(bot2_path, "rb") as f:
            bot2_content = f.read()

        filename1 = "bot1.py"
        filename2 = "bot2.py"

        bot1_content = BytesIO(bot1_content).getvalue()
        bot2_content = BytesIO(bot2_content).getvalue()
        response = client.post(
            "/run-match",
            data={
                "game": game_name,
                "file1": bot1_content,
                "file2": bot2_content,
                "filename1": filename1,
                "filename2": filename2,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "winner" in data
        assert "states" in data
        self.assertIn(data["winner"], [filename1, filename2, None])
        assert len(data["states"]) > 100


class TestValidation(unittest.TestCase):
    def test_valid_bot(self):
        game_name = "dots_and_boxes"
        bot1_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"

        with open(bot1_path, "rb") as f:
            bot1_content = BytesIO(f.read())

        bot1_content = bot1_content.getvalue()
        response = client.post(
            "/validate",
            data={
                "game": game_name,
                "file": bot1_content,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "message" in data
        self.assertEqual(data["success"], True)

    def test_invalid_bot(self):
        game_name = "dots_and_boxes"
        bot1_path = "docker/tests/sample_bots/unsafe_behaviour/runtime_error.py"

        with open(bot1_path, "rb") as f:
            bot1_content = BytesIO(f.read())

        bot1_content = bot1_content.getvalue()
        response = client.post(
            "/validate",
            data={
                "game": game_name,
                "file": bot1_content,
            },
        )
        assert response.status_code == 200
        data = response.json()
        print(data)
        assert "success" in data
        assert "error" in data
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], "Bot does not meet runtime limits.")


if __name__ == "__main__":
    unittest.main()
