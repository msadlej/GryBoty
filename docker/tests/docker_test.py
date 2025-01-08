import requests


# The URL of the FastAPI app running inside Docker
# url = "http://localhost:8080/validate"

# Prepare the data to send
game_name = "morris"
# file_path = "/home/kosla/Studies/pzsp2/project/docker/tests/sample_bots/unsafe_behaviour/runtime_error.py"
# with open(file_path, "rb") as f:
#     files = {"file": f}
#     data = {"game": game_name}

#     # Send the POST request with the file
#     response = requests.post(url, data=data, files=files)

url = "http://localhost:8080/run-match"
bot1_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"
bot2_path = "docker/src/bots/example_bots/testing_bots/bot_2.py"

with open(bot1_path, "rb") as f1, open(bot2_path, "rb") as f2:
    data = {"game": game_name}
    files = {
        "file1": f1,
        "file2": f2,
    }
    response = requests.post(url, data=data, files=files)

print(response.json())
