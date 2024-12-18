from typing import Any
import subprocess
import shlex
import json
import os


DOCKER_DIR = "../docker"
DOCKER_BUILD = "docker build -t game-container -f Dockerfile ."


def run_command(command: str) -> dict[str, Any]:
    """
    Execute a shell command and capture its output
    """

    try:
        split_command = shlex.split(command)
        process = subprocess.Popen(
            split_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()

        return {
            "success": process.returncode == 0,
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
            "return_code": process.returncode,
        }

    except Exception as e:
        return {"success": False, "error": str(e), "type": type(e).__name__}


def run_docker_commands(
    docker_build: str, docker_run: str, base_dir: str | None = None
) -> dict[str, Any]:
    """
    Run Docker build and commands with directory change
    """

    if base_dir is None:
        base_dir = os.getcwd()

    try:
        original_dir = os.getcwd()

        try:
            os.chdir(base_dir)
            print(f"Changed directory to {os.getcwd()}")

            build_result = run_command(docker_build)
            if not build_result["success"]:
                return build_result

            run_result = run_command(docker_run)
            return run_result

        finally:
            os.chdir(original_dir)

    except Exception as e:
        return {"success": False, "error": str(e), "type": type(e).__name__}


def run_game(
    bot_1: str = "src/bots/example_bots/SixMensMorris/bot_1.py",
    bot_2: str = "src/bots/example_bots/SixMensMorris/bot_2.py",
) -> dict[str, Any] | None:
    """
    Run an example game using Docker
    """

    docker_run: str = " ".join(
        (
            "docker run -it",
            f"-v {os.getcwd()}/src:/src",
            "-w /code",
            "game-container",
            "python src/app/services/bot_runner.py",
            "src/two_player_games/games/morris.py SixMensMorris",
            f"{bot_1}",
            f"{bot_2}",
        )
    )

    result: dict[str, Any] = run_docker_commands(DOCKER_BUILD, docker_run, DOCKER_DIR)
    if not result["success"]:
        return None

    data: dict[str, Any] | None = json.loads(result["stdout"])
    return data
