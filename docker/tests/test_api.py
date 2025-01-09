import unittest
from fastapi.testclient import TestClient
from main import app  # Replace with your actual app module

client = TestClient(app)


class TestRunMatch(unittest.TestCase):
    def test_typical_match(self):
        game_name = "dots_and_boxes"
        bot1_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"
        bot2_path = "docker/src/bots/example_bots/testing_bots/bot_2.py"

        with open(bot1_path, "rb") as f1, open(bot2_path, "rb") as f2:
            response = client.post(
                "/run-match",
                data={"game": game_name},
                files={
                    "file1": f1,
                    "file2": f2,
                },
            )
        mock_file_name_1 = "bot_1.py"
        mock_file_name_2 = "bot_2.py"
        assert response.status_code == 200
        data = response.json()
        assert "winner" in data
        assert "states" in data
        self.assertIn(data["winner"], [mock_file_name_1, mock_file_name_2, None])
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
