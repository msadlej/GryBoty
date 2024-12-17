import subprocess
import os


def run_docker_commands():
    try:
        # Build the Docker image
        build_command = [
            "docker",
            "build",
            "-t",
            "game-container",
            "-f",
            "../bots/docker/run_game/Dockerfile",
            "../bots",
        ]
        build_process = subprocess.run(
            build_command, capture_output=True, text=True, check=True
        )
        print("Build Output:", build_process.stdout)

        # Get the current working directory
        current_dir = os.getcwd()

        # Run the Docker container
        run_command = [
            "docker",
            "run",
            "-v",
            f"{current_dir}/../bots/src:/src",
            "-w",
            "/src",
            "game-container",
            "python",
            "app/services/bot_runner.py",
            "two_player_games/games/morris.py",
            "SixMensMorris",
            "bots/example_bots/SixMensMorris/bot_1.py",
            "bots/example_bots/SixMensMorris/bot_2.py",
        ]
        run_process = subprocess.run(
            run_command, capture_output=True, text=True, check=True
        )
        print("Run Output:", run_process.stdout)

        return build_process.stdout, run_process.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return e.stderr, None


# Example usage
if __name__ == "__main__":
    build_logs, run_logs = run_docker_commands()
    print("Build Logs:", build_logs)
    print("Run Logs:", run_logs)
    print("Winer: ", run_logs.split(",")[0][1:])
