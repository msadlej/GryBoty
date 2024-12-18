# Opis zmian
- Dodałem dwa boty w katalogu `src/bots/example_bots/SixMensMorris` - te boty wykorzystamy w prezentacji
- `src/app/services/bot_runner.py` uruchamia rozgrywkę dla danych botów i gry; podaje się jako argumenty wywołania z linii komend:
     - `plik_gry.py` - np. `src/two_player_games/games/morris.py`,
     - nazwa głównej klasy gry (string) - np. `SixMensMorris`,
     - `plik_bot_1.py` - np. `src/bots/example_bots/SixMensMorris/bot_1.py`,
     - `plik_bot_2.py` - np. `src/bots/example_bots/SixMensMorris/bot_2.py`
- Do `bot_runner.py` napisałem kilka testów
- `bot_runner.py` zwraca krotkę: (`ścieżka pliku bota, który wygrał rozgrywkę lub None (gdy remis)`, `słownik z zapisanymi ruchami botów (klucze słownika to ścieżki plików botów)`)

# Uruchomienie gry w kontenerze
Dockerfile znajduje się w katalogu `docker/`


W katalogu 'docker/' projektu:
```bash
docker build -t game-container -f Dockerfile .

docker run -it -v $(pwd)/src:/src -w /code   game-container python src/app/services/bot_runner.py     src/two_player_games/games/morris.py SixMensMorris     src/bots/example_bots/SixMensMorris/bot_1.py     src/bots/example_bots/SixMensMorris/bot_2.py
```
**Na chwilę obecną `bot_runner.py` printuje wynik**

Rezultat przykładowego uruchomienia:
```bash
docker run -it -v $(pwd)/src:/src -w /code   game-container python src/app/services/bot_runner.py     src/two_player_games/games/morris.py SixMensMorris     src/bots/example_bots/SixMensMorris/bot_1.py     src/bots/example_bots/SixMensMorris/bot_2.py

{"winner": "src/bots/example_bots/SixMensMorris/bot_2.py", "moves": ["Gracz 1: Umieszczenie pionka na polu 5", "Gracz 2: Umieszczenie pionka na polu 4", "Gracz 1: Umieszczenie pionka na polu 12", "Gracz 2: Umieszczenie pionka na polu 6", "Gracz 1: Umieszczenie pionka na polu 13", "Gracz 2: Umieszczenie pionka na polu 11", "Gracz 1: Umieszczenie pionka na polu 14, usunięcie pionka przeciwnika z pola 4", "Gracz 2: Umieszczenie pionka na polu 1", "Gracz 1: Umieszczenie pionka na polu 9", "Gracz 2: Umieszczenie pionka na polu 2", "Gracz 1: Umieszczenie pionka na polu 8", "Gracz 2: Umieszczenie pionka na polu 7", "Gracz 1: Przesunięcie pionka z pola 9 na pole 10", "Gracz 2: Przesunięcie pionka z pola 11 na pole 3", "Gracz 1: Przesunięcie pionka z pola 12 na pole 11", "Gracz 2: Przesunięcie pionka z pola 1 na pole 0, usunięcie pionka przeciwnika z pola 10", "Gracz 1: Przesunięcie pionka z pola 5 na pole 4", "Gracz 2: Przesunięcie pionka z pola 0 na pole 1", "Gracz 1: Przesunięcie pionka z pola 11 na pole 12, usunięcie pionka przeciwnika z pola 2", "Gracz 2: Przesunięcie pionka z pola 1 na pole 0, usunięcie pionka przeciwnika z pola 8", "Gracz 1: Przesunięcie pionka z pola 13 na pole 5", "Gracz 2: Przesunięcie pionka z pola 3 na pole 11", "Gracz 1: Przesunięcie pionka z pola 5 na pole 13, usunięcie pionka przeciwnika z pola 11", "Gracz 2: Przesunięcie pionka z pola 7 na pole 15", "Gracz 1: Przesunięcie pionka z pola 12 na pole 11", "Gracz 2: Przesunięcie pionka z pola 15 na pole 7, usunięcie pionka przeciwnika z pola 4", "Gracz 1: Przesunięcie pionka z pola 14 na pole 15", "Gracz 2: Przesunięcie pionka z pola 6 na pole 5", "Gracz 1: Przesunięcie pionka z pola 11 na pole 10", "Gracz 2: Przesunięcie pionka z pola 0 na pole 1", "Gracz 1: Przesunięcie pionka z pola 13 na pole 12", "Gracz 2: Przesunięcie pionka z pola 5 na pole 6", "Gracz 1: Przesunięcie pionka z pola 10 na pole 9", "Gracz 2: Przesunięcie pionka z pola 1 na pole 0, usunięcie pionka przeciwnika z pola 15"]}
```
