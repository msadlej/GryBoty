import requests


# The URL of the FastAPI app running inside Docker
url = "http://localhost:8080/validate"

# Prepare the data to send
game_name = "morris"
file_path = "/home/kosla/Studies/pzsp2/project/docker/tests/sample_bots/unsafe_behaviour/runtime_error.py"
with open(file_path, "rb") as f:
    files = {"file": f}
    data = {"game": game_name}

    # Send the POST request with the file
    response = requests.post(url, data=data, files=files)

print(response.json())
