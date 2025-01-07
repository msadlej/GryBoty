import requests
from io import BytesIO




# The URL of the FastAPI app running inside Docker
url = "http://localhost:8080/validate"

# Prepare the data to send
game_name = "morris"
file_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"

# Prepare the files and form data
with open(file_path, "rb") as f:
    bot = f.read()


bot_file = BytesIO(bot).getvalue()

files = {"file": bot_file}  # Open the file in binary mode
data = {"game": game_name}

data = {"game": game_name, "file": bot_file}

# Send the POST request
response = requests.post(url, data=data)

# Print the response from FastAPI
print(response.json())
