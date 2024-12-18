import React, { useState } from 'react';

const BackButton = ({ onNavigate, to = 'dashboard' }) => (
  <button
    onClick={() => onNavigate(to)}
    className="absolute top-8 left-8 bg-button-bg text-white px-6 py-3 rounded hover:bg-button-hover text-xl font-light"
  >
    ← Powrót
  </button>
);

const LoginScreen = ({ onNavigate }) => {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <h1 className="text-5xl mb-12 font-light">Zaloguj się</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Login:</label>
          <input 
            type="text" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Hasło:</label>
          <input 
            type="password" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div className="flex justify-between pt-6">
          <button 
            onClick={() => onNavigate('register')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Zarejestruj się
          </button>
          <button 
            onClick={() => onNavigate('dashboard')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Zaloguj się
          </button>
        </div>
      </div>
    </div>
  );
};

const RegisterScreen = ({ onNavigate }) => {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="login" />
      <h1 className="text-5xl mb-12 font-light">Zarejestruj się</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Login:</label>
          <input 
            type="text" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Hasło:</label>
          <input 
            type="password" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Powtórz:</label>
          <input 
            type="password" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <button 
          onClick={() => onNavigate('dashboard')}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Zarejestruj
        </button>
      </div>
    </div>
  );
};

const SettingsScreen = ({ onNavigate }) => {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} />
      <h1 className="text-5xl mb-12 font-light">Ustawienia</h1>
      <div className="w-full max-w-[80%]">
        <button 
          className="w-full bg-button-bg text-white px-12 py-6 rounded hover:bg-button-hover text-2xl font-light"
          onClick={() => onNavigate('change-password')}
        >
          Zmień hasło
        </button>
      </div>
    </div>
  );
};

const ChangePasswordScreen = ({ onNavigate }) => {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="settings" />
      <h1 className="text-5xl mb-12 font-light">Zmień hasło</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Stare hasło:</label>
          <input 
            type="password" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Nowe hasło:</label>
          <input 
            type="password" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Powtórz:</label>
          <input 
            type="password" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <button 
          onClick={() => onNavigate('settings')}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Zmień
        </button>
      </div>
    </div>
  );
};

const DashboardScreen = ({ onNavigate }) => {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <h1 className="text-5xl mb-12 font-light">Boty gierki</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <button 
          className="w-full bg-button-bg text-white px-12 py-6 rounded hover:bg-button-hover text-2xl font-light"
          onClick={() => onNavigate('tournaments')}
        >
          Twoje turnieje
        </button>
        <button 
          className="w-full bg-button-bg text-white px-12 py-6 rounded hover:bg-button-hover text-2xl font-light"
          onClick={() => onNavigate('bots')}
        >
          Twoje boty
        </button>
        <button 
          className="w-full bg-button-bg text-white px-12 py-6 rounded hover:bg-button-hover text-2xl font-light"
          onClick={() => onNavigate('settings')}
        >
          Ustawienia
        </button>
        <button 
          className="w-full bg-button-bg text-white px-12 py-6 rounded hover:bg-button-hover text-2xl font-light"
          onClick={() => onNavigate('login')}
        >
          Wyloguj się
        </button>
      </div>
    </div>
  );
};

const TournamentsScreen = ({ onNavigate }) => {
  const tournaments = [
    { name: "Turniej o Złotą Kredę", startTime: "13.11.2024 14:00", organizer: "Adam" },
    { name: "testturniej3", startTime: "19.12.2024 21:40", organizer: "Jakub" }
  ];

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} />
      <h1 className="text-5xl mb-12 font-light">Turnieje</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div className="grid grid-cols-3 gap-4 text-2xl font-light mb-4">
          <div>Nazwa</div>
          <div>Rozpoczęcie</div>
          <div>Organizator</div>
        </div>
        {tournaments.map((tournament, index) => (
          <div 
            key={index} 
            className="grid grid-cols-3 gap-4 bg-button-bg p-4 rounded cursor-pointer hover:bg-button-hover transition-colors"
            onClick={() => onNavigate('tournament-tree')}
          >
            <div className="hover:underline">{tournament.name}</div>
            <div>{tournament.startTime}</div>
            <div>{tournament.organizer}</div>
          </div>
        ))}
        <div className="flex justify-between mt-8">
          <button
            onClick={() => onNavigate('join-tournament')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Dołącz do turnieju
          </button>
          <button
            onClick={() => onNavigate('create-tournament')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Stwórz turniej
          </button>
        </div>
      </div>
    </div>
  );
};

const CreateTournamentScreen = ({ onNavigate }) => {
  const games = ["Kółko i krzyżyk", "Czwórki", "Warcaby"];
  
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-12 font-light">Stwórz turniej</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Nazwa:</label>
          <input 
            type="text"
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Opis:</label>
          <input 
            type="text"
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Gra:</label>
          <select className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light">
            {games.map(game => (
              <option key={game} value={game}>{game}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-2xl font-light">Czas rozpoczęcia:</label>
          <input 
            type="datetime-local"
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Limit graczy:</label>
          <input 
            type="number"
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <button 
          onClick={() => onNavigate('tournaments')}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Stwórz
        </button>
      </div>
    </div>
  );
};

const BotsListScreen = ({ onNavigate }) => {
  const bots = [
    { name: "testbot1", game: "Czwórki" },
    { name: "testbot2", game: "Kółko i krzyżyk" },
    { name: "gigabot", game: "Czwórki" }
  ];

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} />
      <h1 className="text-5xl mb-12 font-light">Boty</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div className="grid grid-cols-3 gap-4 text-2xl font-light mb-4">
          <div>Nazwa</div>
          <div>Gra</div>
          <div></div>
        </div>
        {bots.map((bot, index) => (
          <div 
            key={index} 
            className="grid grid-cols-3 gap-4 bg-button-bg p-4 rounded cursor-pointer hover:bg-button-hover transition-colors"
            onClick={() => onNavigate('bot-details')}
          >
            <div className="hover:underline">{bot.name}</div>
            <div>{bot.game}</div>
            <button 
              className="bg-button-hover text-white px-6 py-2 rounded hover:bg-primary-bg justify-self-end"
              onClick={(e) => {
                e.stopPropagation();
                alert('Usuwanie bota');
              }}
            >
              Usuń
            </button>
          </div>
        ))}
        <button
          onClick={() => onNavigate('add-bot')}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light mt-8"
        >
          Dodaj bota
        </button>
      </div>
    </div>
  );
};

const AddBotScreen = ({ onNavigate }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const games = ["Kółko i krzyżyk", "Czwórki", "Warcaby"];
  const fileInputRef = React.useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragging(true);
    } else if (e.type === "dragleave") {
      setIsDragging(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      validateAndSetFile(files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file) => {
    if (file.name.endsWith('.py')) {
      setSelectedFile(file);
    } else {
      alert('Proszę wybrać plik z rozszerzeniem .py');
    }
  };

  const dropzoneStyle = `
    w-full h-48 
    border-2 border-dashed rounded 
    flex flex-col items-center justify-center 
    cursor-pointer 
    transition-colors
    ${isDragging 
      ? 'border-white bg-button-hover' 
      : 'border-button-bg bg-button-bg hover:bg-button-hover'
    }
    ${selectedFile 
      ? 'bg-button-hover' 
      : ''
    }
  `;

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="bots" />
      <h1 className="text-5xl mb-12 font-light">Dodaj bota</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Nazwa:</label>
          <input 
            type="text"
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            placeholder="Nazwa twojego bota"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Gra:</label>
          <select className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light">
            {games.map(game => (
              <option key={game} value={game}>{game}</option>
            ))}
          </select>
        </div>

        {}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept=".py"
          className="hidden"
        />

        {}
        <div
          className={dropzoneStyle}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          {selectedFile ? (
            <>
              <div className="text-4xl mb-4">✓</div>
              <div className="text-xl font-light">{selectedFile.name}</div>
              <div className="text-sm font-light mt-2">Kliknij aby zmienić plik</div>
            </>
          ) : (
            <>
              <div className="text-4xl mb-4">↓</div>
              <div className="text-xl font-light">
                {isDragging ? 'Upuść plik tutaj' : 'Wrzuć plik .py'}
              </div>
              <div className="text-sm font-light mt-2">lub kliknij aby wybrać</div>
            </>
          )}
        </div>

        <button 
          onClick={() => onNavigate('bots')}
          className={`w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light
            ${!selectedFile ? 'opacity-50 cursor-not-allowed' : ''}`}
          disabled={!selectedFile}
        >
          Dodaj
        </button>
      </div>
    </div>
  );
};

const BotDetailsScreen = ({ onNavigate }) => {
  const bot = {
    name: "testbot1",
    totalGames: 65,
    wins: 34,
    tournaments: [
      { name: "Turniej o Złotą Kredę", date: "13.11.2024 14:00" },
      { name: "testturniej3", date: "19.12.2024 21:40" }
    ]
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="bots" />
      <h1 className="text-5xl mb-12 font-light">Bot: {bot.name}</h1>
      <div className="w-full max-w-[80%] space-y-8">
        <div className="space-y-4">
          <h2 className="text-3xl font-light mb-6">Statystyki:</h2>
          <div className="text-xl font-light">Liczba gier: {bot.totalGames}</div>
          <div className="text-xl font-light">Liczba wygranych: {bot.wins}</div>
        </div>
        <div className="space-y-4">
          <h2 className="text-3xl font-light mb-6">Historia turniejów:</h2>
          {bot.tournaments.map((tournament, index) => (
            <div 
              key={index} 
              className="bg-button-bg p-4 rounded flex justify-between cursor-pointer hover:bg-button-hover transition-colors"
              onClick={() => onNavigate('tournament-tree')}
            >
              <div className="hover:underline">{tournament.name}</div>
              <div>{tournament.date}</div>
            </div>
          ))}
        </div>
        <button 
          onClick={() => onNavigate('bots')}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Usuń bota
        </button>
      </div>
    </div>
  );
};

const JoinTournamentScreen = ({ onNavigate }) => {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-12 font-light">Dołącz do turnieju</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Kod dostępu:</label>
          <input 
            type="text" 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <button 
          onClick={() => onNavigate('select-bot')}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Zmień
        </button>
      </div>
    </div>
  );
};

const SelectBotScreen = ({ onNavigate }) => {
  const tournamentInfo = {
    name: "testturniej1",
    game: "Kółko i krzyżyk",
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="join-tournament" />
      <h1 className="text-5xl mb-12 font-light">Dołączasz do turnieju {tournamentInfo.name}</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div className="text-2xl font-light mb-8">Gra: {tournamentInfo.game}</div>
        <div>
          <label className="text-2xl font-light">Wybierz bota:</label>
          <select className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light">
            <option value="testbot2">testbot2</option>
          </select>
        </div>
        <button 
          onClick={() => onNavigate('tournaments')}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Dołącz
        </button>
      </div>
    </div>
  );
};

const ManageTournamentScreen = ({ onNavigate }) => {
  const tournamentData = {
    name: "testturniej1",
    description: "",
    startTime: "2024-11-13T14:30",
    playerLimit: 8,
    participants: [
      "Jakub",
      "Adam",
      "Michał"
    ]
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-12 font-light">Zarządzaj: {tournamentData.name}</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Nazwa:</label>
          <input 
            type="text"
            value={tournamentData.name}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Opis:</label>
          <input 
            type="text"
            value={tournamentData.description}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Czas rozpoczęcia:</label>
          <input 
            type="datetime-local"
            value={tournamentData.startTime}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Limit graczy:</label>
          <input 
            type="number"
            value={tournamentData.playerLimit}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div className="space-y-4">
          <label className="text-2xl font-light">Uczestnicy:</label>
          {tournamentData.participants.map((participant, index) => (
            <div key={index} className="flex justify-between items-center bg-button-bg p-4 rounded">
              <span className="text-xl font-light">{participant}</span>
              <button 
                className="bg-button-hover px-6 py-2 rounded hover:bg-button-bg"
              >
                Usuń
              </button>
            </div>
          ))}
        </div>
        <div className="flex justify-between mt-8">
          <button 
            onClick={() => onNavigate('tournaments')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Anuluj turniej
          </button>
          <button 
            onClick={() => onNavigate('tournament-tree')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Rozpocznij turniej
          </button>
        </div>
      </div>
    </div>
  );
};

const TournamentMatchScreen = ({ onNavigate }) => {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournament-tree" />
      <h1 className="text-5xl mb-12 font-light">Mecz: Adam vs Michał</h1>
      <div className="w-full max-w-[80%] space-y-6">
        <h2 className="text-3xl font-light text-center">Turniej o Złotą Kredę</h2>
        <div className="text-2xl font-light text-center mb-12">Wygrana:</div>
        <h3 className="text-2xl font-light mb-4">Historia ruchów:</h3>
        <div className="h-64 bg-button-bg rounded"></div>
      </div>
    </div>
  );
};

const TournamentTreeScreen = ({ onNavigate }) => {
  const TournamentNode = ({ label, players }) => (
    <div 
      className="bg-button-bg px-8 py-2 rounded cursor-pointer hover:bg-button-hover transition-colors"
      onClick={() => onNavigate('tournament-match')}
    >
      {players ? 
        <div className="text-center hover:underline">{players[0]} vs {players[1]}</div> :
        <div>{label}</div>
      }
    </div>
  );

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-4 font-light">Turniej: testturniej1</h1>
      <div className="text-2xl font-light mb-2">Rozpoczęcie: 13.11.2024 14:30</div>
      <div className="text-2xl font-light mb-12">Kod: 7590</div>
      <div className="w-full max-w-[80%] space-y-6">
        <div className="flex flex-col items-center space-y-12">
          <TournamentNode label="Finał" players={['Adam', 'Jakub']} />
          <div className="flex justify-around w-full">
            <TournamentNode label="P-finał" players={['Adam', 'Michał']} />
            <TournamentNode label="P-finał" players={['Jakub', 'Olek']} />
          </div>
          <div className="flex justify-around w-full">
            <TournamentNode label="Ć-finał" players={['Adam', 'Sebek']} />
            <TournamentNode label="Ć-finał" players={['Michał', 'Maciej']} />
            <TournamentNode label="Ć-finał" players={['Jakub', 'Łukasz']} />
            <TournamentNode label="Ć-finał" players={['Olek', 'Bartek']} />
          </div>
        </div>
        <div className="flex justify-center mt-12">
          <button 
            onClick={() => onNavigate('manage-tournament')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Zarządzaj
          </button>
        </div>
      </div>
    </div>
  );
};

const App = () => {
  const [currentScreen, setCurrentScreen] = useState('login');

  const screens = {
    'login': LoginScreen,
    'register': RegisterScreen,
    'dashboard': DashboardScreen,
    'settings': SettingsScreen,
    'change-password': ChangePasswordScreen,
    'tournaments': TournamentsScreen,
    'create-tournament': CreateTournamentScreen,
    'bots': BotsListScreen,
    'add-bot': AddBotScreen,
    'bot-details': BotDetailsScreen,
    'join-tournament': JoinTournamentScreen,
    'select-bot': SelectBotScreen,
    'manage-tournament': ManageTournamentScreen,
    'tournament-match': TournamentMatchScreen,
    'tournament-tree': TournamentTreeScreen,
  };

  const CurrentComponent = screens[currentScreen];

  return <CurrentComponent onNavigate={setCurrentScreen} />;
};

export default App;
