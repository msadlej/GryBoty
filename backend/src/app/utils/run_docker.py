import os
import subprocess
import shlex


class DockerCommandRunner:
    def __init__(self, base_dir=None):
        """
        Initialize Docker command runner with optional base directory

        :param base_dir: Base directory to change to before running commands
        """
        self.base_dir = base_dir or os.getcwd()

    def run_docker_commands(self, build_command, run_command):
        """
        Run Docker build and run commands with directory change

        :param build_command: Docker build command
        :param run_command: Docker run command
        :return: Dictionary with execution results
        """
        try:
            # Store the current working directory
            original_dir = os.getcwd()

            try:
                # Change to the specified base directory
                os.chdir(self.base_dir)

                # Execute build command
                build_result = self._run_command(build_command)
                if not build_result["success"]:
                    return build_result

                # Execute run command
                run_result = self._run_command(run_command)

                return run_result

            finally:
                # Always change back to the original directory
                os.chdir(original_dir)

        except Exception as e:
            return {"success": False, "error": str(e), "type": type(e).__name__}

    def _run_command(self, command):
        """
        Execute a shell command and capture its output

        :param command: Command to execute
        :return: Dictionary with command execution results
        """
        try:
            # Split the command to handle both simple and complex commands
            split_command = shlex.split(command)

            # Run the command and capture output
            process = subprocess.Popen(
                split_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            # Capture stdout and stderr
            stdout, stderr = process.communicate()

            return {
                "success": process.returncode == 0,
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "return_code": process.returncode,
            }

        except Exception as e:
            return {"success": False, "error": str(e), "type": type(e).__name__}


def run_game():
    # Specify the directory containing your Docker context
    docker_dir = "../docker"

    # Build command
    build_cmd = "docker build -t game-container -f docker/run_game/Dockerfile ."

    # Run command (note: $(pwd) is replaced with actual path handling in Python)
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

    # Create runner
    runner = DockerCommandRunner(base_dir=docker_dir)

    # Execute commands
    result = runner.run_docker_commands(build_cmd, run_cmd)

    # Return match winner
    return result["stdout"] if result["success"] else result["stderr"]
