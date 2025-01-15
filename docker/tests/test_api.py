import unittest
from fastapi.testclient import TestClient
from main import app  # Replace with your actual app module
import io

client = TestClient(app)


class TestRunMatch(unittest.TestCase):
    def test_typical_match(self):
        game_name = "dots_and_boxes"
        bot1_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"
        bot2_path = "docker/src/bots/example_bots/testing_bots/bot_2.py"

        with open(bot1_path, "rb") as f1, open(bot2_path, "rb") as f2:
            bot_1 = io.BytesIO(f1.read())
            bot_2 = io.BytesIO(f2.read())

        response = client.post(
            "/run-match",
            data={"game": game_name},
            files={"file1": bot_1, "file2": bot_2},
        )

        assert response.status_code == 200
        data = response.json()
        assert "winner" in data
        assert "states" in data
        self.assertIn(data["winner"], [0, 1, None])
        assert len(data["states"]) > 100


class TestValidation(unittest.TestCase):
    def test_valid_bot(self):
        game_name = "dots_and_boxes"
        bot1_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"

        with open(bot1_path, "rb") as f:
            response = client.post(
                "/validate",
                data={"game": game_name},
                files={"file": f},
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
            response = client.post(
                "/validate",
                data={"game": game_name},
                files={"file": f},
            )
        assert response.status_code != 200
        data = response.json()
        assert data["detail"] == "Bot does not meet runtime limits."


if __name__ == "__main__":
    unittest.main()
