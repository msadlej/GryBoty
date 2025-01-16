from fastapi import HTTPException, status
from typing import Any
import requests


def validate_bot(game_name: str, code: bytes) -> bool:
    """
    Validates a bot for a specific game.
    Returns True if the bot is valid, otherwise raises an HTTPException with error details.
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

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_details
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {response.status_code}",
        )


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

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_message
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {response.status_code}",
        )
