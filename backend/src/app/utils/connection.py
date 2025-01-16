from typing import Any
import requests


def validate_bot(game_name: str, code: bytes) -> bool:
    """
    Validates a bot for a specific game.
    Returns True if the bot is valid, False otherwise.
    """

    files = {"file": code}
    data = {"game": game_name}
    url = "http://localhost:8080/validate"
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        response_data = response.json()
        result: bool = response_data.get("success", False)

        return result
    elif response.status_code == 400:
        response_data = response.json()
        error_details = response_data.get("detail", [])
        print(f"Validation failed: {error_details}")

        return False
    else:
        print(f"Unexpected error: {response.status_code}")

        return False


def run_match(game_name: str, bot1_code: bytes, bot2_code: bytes) -> dict[str, Any]:
    """
    Runs a match between two bots for a specific game.
    Returns the match result as a dictionary.
    """

    files = {"file1": bot1_code, "file2": bot2_code}
    data = {"game": game_name}
    url = "http://localhost:8080/run-match"
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        result: dict[str, Any] = response.json()

        return result
    elif response.status_code == 400:
        response_data = response.json()
        error_message = response_data.get("detail", "Unknown error")
        print(f"Match failed: {error_message}")

        return {"error": error_message}
    else:
        print(f"Unexpected error: {response.status_code}")

        return {"error": f"Unexpected error: {response.status_code}"}
