# Uruchamianie środowiska botów

```bash
docker compose-up --build
```
or
```bash
docker-compose up --build
```

# Dostęp
API działa na porcie `8080` i udostępnia dwa endpointy:
1. Walidacja bota: `/validate`:
    - Metoda `POST`
    - Parametry: 
        - `game` (string): Nazwa gry spośród `nim`, `dots_and_boxes`, `pick`, `morris`, `connect_four`
        - `file` (UploadFile): Plik zawierający kod bota do walidacji
 
2. Uruchamianie mecz: `/run-match`:
    - Metoda: `POST`
    - Parametry:
        - `game` (string): Nazwa gry.
        - `file1` (UploadFile): Plik z kodem pierwszego bota.
        - `file2` (UploadFile): Plik z kodem drugiego bota.

# Wyniki
1. **Walidacja bota** 

    Zwraca odpowiedź JSON:

   ```json
   {
       "success": true,
       "message": "Validation passed."
   }
    ```
    
    W przypadku błędu zwracany jest komunikat o błędzie z kodem statusu 400. Przykład odpowiedzi w przypadku błędnej walidacji:

```json
{
    "detail": [
        {
            // error details to show the user!
        }
    ]
}
```

2. **Uruchomienie meczu** 
    
    Zwraca odpowiedź JSON z wynikiem meczu oraz stanem gry:
```json
{
    "winner": "bot1",  // Winner filename (from UploadFile)
    "states": "[state1, state2, state3]"  // states
}
```

W przypadku błędu w trakcie rozgrywki, zwrócony zostanie komunikat o błędzie w formacie JSON:

```json
{
    "detail": "Error message describing what went wrong"
}
```
Tutaj zakładamy, że żadne błędy nie będą występować, zwracane błędy służą jedynie podczas procesu developmentu.

# Przykłady

## Walidacja bota

```python
import requests

url = "http://localhost:8080/validate"

# Prepare the data to send
game_name = "morris"    # game name
file_path = "docker/tests/sample_bots/unsafe_behaviour/runtime_error.py" # mock bot
with open(file_path, "rb") as f:    # read bot as binary (UploadFile in app)
    files = {"file": f} # bot to validate
    data = {"game": game_name}  # game name

    # Send the POST request with the file
    response = requests.post(url, data=data, files=files)

```

## Uruchamienie meczu

```python
game_name = "morris"

url = "http://localhost:8080/run-match"
bot1_path = "docker/src/bots/example_bots/testing_bots/bot_1.py"
bot2_path = "docker/src/bots/example_bots/testing_bots/bot_2.py"

with open(bot1_path, "rb") as f1, open(bot2_path, "rb") as f2:
    data = {"game": game_name} # game name
    files = {
        "file1": f1,    # first bot
        "file2": f2,    # second bot
    }
    response = requests.post(url, data=data, files=files)

```