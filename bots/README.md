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
Dockerfile znajduje się w katalogu `docker/run_game`


W katalogu głównym projektu:
```bash
docker build -t game-container -f docker/run_game/Dockerfile .

docker run -it -v $(pwd)/src:/src -w /code   game-container python src/app/services/bot_runner.py     src/two_player_games/games/morris.py SixMensMorris     src/bots/example_bots/SixMensMorris/bot_1.py     src/bots/example_bots/SixMensMorris/bot_2.py
```
**Na chwilę obecną `bot_runner.py` printuje wynik**

Rezultat przykładowego uruchomienia:
```bash
docker run -it -v $(pwd)/src:/src -w /code   game-container python src/app/services/bot_runner.py     src/two_player_games/games/morris.py SixMensMorris     src/bots/example_bots/SixMensMorris/bot_1.py     src/bots/example_bots/SixMensMorris/bot_2.py
          
('src/bots/example_bots/SixMensMorris/bot_2.py', {'src/bots/example_bots/SixMensMorris/bot_1.py': [<morris.MorrisMove object at 0x781a734feed0>, <morris.MorrisMove object at 0x781a734ff0d0>, <morris.MorrisMove object at 0x781a734ff1d0>, <morris.MorrisMove object at 0x781a734ff090>, <morris.MorrisMove object at 0x781a734ff410>, <morris.MorrisMove object at 0x781a734ff350>, <morris.MorrisMove object at 0x781a734ff790>, <morris.MorrisMove object at 0x781a734ff7d0>, <morris.MorrisMove object at 0x781a734ffa50>, <morris.MorrisMove object at 0x781a734ffbd0>, <morris.MorrisMove object at 0x781a734ffc90>, <morris.MorrisMove object at 0x781a734ffe10>, <morris.MorrisMove object at 0x781a734fff10>, <morris.MorrisMove object at 0x781a735041d0>, <morris.MorrisMove object at 0x781a735042d0>], 'src/bots/example_bots/SixMensMorris/bot_2.py': [<morris.MorrisMove object at 0x781a734fefd0>, <morris.MorrisMove object at 0x781a734ff110>, <morris.MorrisMove object at 0x781a734ff150>, <morris.MorrisMove object at 0x781a734ff390>, <morris.MorrisMove object at 0x781a734ff510>, <morris.MorrisMove object at 0x781a734ff810>, <morris.MorrisMove object at 0x781a734ff890>, <morris.MorrisMove object at 0x781a734ffa10>, <morris.MorrisMove object at 0x781a734ff850>, <morris.MorrisMove object at 0x781a734ff9d0>, <morris.MorrisMove object at 0x781a734ffed0>, <morris.MorrisMove object at 0x781a734fff50>, <morris.MorrisMove object at 0x781a73504150>, <morris.MorrisMove object at 0x781a73504410>, <morris.MorrisMove object at 0x781a73504590>]})
```