# Tworzenie Bota do Gry

Aby dodać bota do systemu, należy przestrzegać kilku zasad i wymagań. Poniżej znajdziesz szczegółowy opis jak stworzyć bota, który będzie zgodny z wymaganiami.

### Warunki dla Bota:
1. **Dozwolone biblioteki**:
   Twój bot może importować jedynie następujące biblioteki:
   - `math`
   - `random`
   - `itertools`
   - `functools`
   - `collections`
   - `numpy`
   - `src.bots.example_bots.example_bot` (Abstrakcyjna klasa Bot, Wymagane)
   - `abc` 
   
2. **Importy dotyczące gry**:
   Twój bot może importować elementy związane z grą poprzez `two_player_game`, takie jak:
   - `two_player_games.move` (dla ruchów)
   - `two_player_games.state` (dla stanu gry)

3. **Zasady nazewnictwa**:
   - Nie możesz używać operatorów takich jak `+=`.
   - Unikaj używania `_` w nazwach atrybutów. **Nie używaj super().__init__()**. 
   - **__init__ jest dozwolone, jednak nie dla klasy, która implementuje bota (dziedziczy po Bot)**

4. **Dziedziczenie po klasie `Bot`**:
   - Twój bot musi dziedziczyć po klasie `Bot`, która jest podstawową klasą bota w systemie.
   - Musi istnieć dokładnie jedna klasa dziedzicząca po `Bot`.

5. **Metoda `get_move`**:
   - Twój bot musi implementować metodę `get_move(self, state: State) -> Move`, która **zwraca odpowiednią klasę ruchu,** np. `MorrisMove`, zgodnie z grą, w której bierze udział.
   - Metoda `get_move` przyjmuje dwa parametry: `self` (instancję bota) oraz `state` (obiekt reprezentujący stan gry).
   
6. **Limit czasu**:
   - Bot nie może przekroczyć 2 sekund na wykonanie ruchu.

### Przykład Poprawnego Bota

Poniżej znajduje się przykładowy kod bota, który spełnia wszystkie wymagania:

```python
from src.bots.example_bots.example_bot import Bot
from two_player_games.move import Move
from two_player_games.state import State
import random

class Bot_1(Bot):
    """
    A simple example implementation of a bot that inherits from the base Bot class.
    
    This bot randomly selects a move from the available moves in the current game state.
    
    NOTE:
    - This is a basic bot and should be replaced or extended with more complex logic
      for competitive play.
    - Class must implement the `get_move` method.
    """

    def get_move(self, state: State) -> Move:
        """
        This method is called to get the next move for the bot based on the current game state.

        :param state: The current state of the game (an instance of State).
        :return: A move object (an instance of Move).
        """
        
        moves = state.get_moves()  # Get available moves from the current game state
        move = random.choice(moves)  # Randomly select a move from available moves
        
        return move  # Return the selected move