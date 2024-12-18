from typing import Any
import subprocess
import shlex
import json
import os


class DockerCommandRunner:
    """Class to run Docker commands"""

    def __init__(self, base_dir: str | None = None):
        """
        Initialize Docker command runner with optional base directory
        """
        self.base_dir = base_dir or os.getcwd()

    def run_docker_commands(self, build_command, run_command):
        """
        Run Docker build and commands with directory change
        """

        try:
            original_dir = os.getcwd()

            try:
                os.chdir(self.base_dir)

                build_result = self._run_command(build_command)
                if not build_result["success"]:
                    return build_result

                run_result = self._run_command(run_command)

                return run_result

            finally:
                os.chdir(original_dir)

        except Exception as e:
            return {"success": False, "error": str(e), "type": type(e).__name__}

    def _run_command(self, command):
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


def run_game() -> dict[str, Any] | None:
    """
    Run an example game using Docker
    """

    docker_dir = "../docker"
    build_cmd = "docker build -t game-container -f Dockerfile ."
    run_cmd = (
        "docker run -it "
        "-v {pwd}/src:/src "
        "-w /code "
        "game-container "
        "python src/app/services/bot_runner.py "
        "src/two_player_games/games/morris.py SixMensMorris "
        "src/bots/example_bots/SixMensMorris/bot_1.py "
        "src/bots/example_bots/SixMensMorris/bot_2.py"
    ).format(pwd=os.getcwd())

    runner = DockerCommandRunner(base_dir=docker_dir)
    result = runner.run_docker_commands(build_cmd, run_cmd)

    if not result["success"]:
        return None

    data: dict[str, Any] | None = json.loads(result["stdout"])
    return data
