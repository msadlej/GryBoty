import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  SingleEliminationBracket,
  Match,
  SVGViewer,
  createTheme
} from '@g-loot/react-tournament-brackets';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  console.log('Interceptor applied:', config);
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

const login = async (username, password) => {
  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/token/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    const { access_token } = response.data;
    localStorage.setItem('token', access_token);
    return response.data;
  } catch (error) {
    console.error('Login error:', error.response?.data);
    throw error;
  }
};

const register = async (username, password) => {
  try {
    const response = await api.post('/users/register/', {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    console.error('Register error:', error.response?.data);
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('token');
};

const BackButton = ({ onNavigate, to = 'dashboard', ...params }) => (
  <button
    onClick={() => onNavigate(to, params)}
    className="absolute top-8 left-8 bg-button-bg text-white px-6 py-3 rounded hover:bg-button-hover text-xl font-light"
  >
    ← Powrót
  </button>
);

export const LoginScreen = ({ onNavigate }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Attempting login with:', {
        username: formData.username,
        password: formData.password
      });
      
      await login(formData.username, formData.password);
      onNavigate('dashboard');
    } catch (err) {
      console.error('Login failed:', err);
      setError('Nieprawidłowy login lub hasło');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <h1 className="text-5xl mb-12 font-light">Zaloguj się</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Login:</label>
          <input 
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({...formData, username: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            disabled={loading}
          />
        </div>
        <div>
          <label className="text-2xl font-light">Hasło:</label>
          <input 
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            disabled={loading}
          />
        </div>
        <div className="flex justify-between pt-6">
          <button 
            type="button"
            onClick={() => onNavigate('register')}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
            disabled={loading}
          >
            Zarejestruj się
          </button>
          <button 
            type="submit"
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
            disabled={loading}
          >
            {loading ? 'Logowanie...' : 'Zaloguj się'}
          </button>
        </div>
      </form>
    </div>
  );
};

export const RegisterScreen = ({ onNavigate }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError('Hasła nie są identyczne');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await register(formData.username, formData.password);
      onNavigate('login');
    } catch (err) {
      setError('Nie udało się zarejestrować użytkownika');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="login" />
      <h1 className="text-5xl mb-12 font-light">Zarejestruj się</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Login:</label>
          <input 
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({...formData, username: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            disabled={loading}
          />
        </div>
        <div>
          <label className="text-2xl font-light">Hasło:</label>
          <input 
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            disabled={loading}
          />
        </div>
        <div>
          <label className="text-2xl font-light">Powtórz:</label>
          <input 
            type="password"
            value={formData.confirmPassword}
            onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            disabled={loading}
          />
        </div>
        <button 
          type="submit"
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
          disabled={loading}
        >
          {loading ? 'Rejestracja...' : 'Zarejestruj'}
        </button>
      </form>
    </div>
  );
};

export const SettingsScreen = ({ onNavigate }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [username, setUsername] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get('/users/me/');
        setUsername(response.data.username);
      } catch (err) {
        setError('Nie udało się pobrać danych użytkownika');
      }
    };

    fetchUser();
  }, []);

  const handleLogout = () => {
    setLoading(true);
    try {
      localStorage.removeItem('token');
      onNavigate('login');
    } catch (err) {
      setError('Nie udało się wylogować');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} />
      <h1 className="text-5xl mb-12 font-light">Ustawienia</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="w-full max-w-[80%] space-y-6">
        <div className="text-2xl font-light mb-8">
          Zalogowany jako: {username}
        </div>
        <button 
          className="w-full bg-button-bg text-white px-12 py-6 rounded hover:bg-button-hover text-2xl font-light"
          onClick={() => onNavigate('change-password')}
        >
          Zmień hasło
        </button>
        <button 
          className="w-full bg-button-bg text-white px-12 py-6 rounded hover:bg-button-hover text-2xl font-light"
          onClick={handleLogout}
          disabled={loading}
        >
          {loading ? 'Wylogowywanie...' : 'Wyloguj się'}
        </button>
      </div>
    </div>
  );
};

export const ChangePasswordScreen = ({ onNavigate }) => {
  const [formData, setFormData] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.newPassword !== formData.confirmPassword) {
      setError('Nowe hasła nie są identyczne');
      return;
    }
  
    if (formData.newPassword.length < 5 || formData.newPassword.length > 32) {
      setError('Nowe hasło musi mieć od 5 do 32 znaków');
      return;
    }
  
    const formDataObj = new FormData();
    formDataObj.append('old_password', formData.oldPassword);
    formDataObj.append('new_password', formData.newPassword);
  
    setLoading(true);
    try {
      await api.put('/users/change_password', formDataObj, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      onNavigate('settings');
    } catch (err) {
      console.log('Change password error:', err);
      setError('Nie udało się zmienić hasła - ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="settings" />
      <h1 className="text-5xl mb-12 font-light">Zmień hasło</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Stare hasło:</label>
          <input 
            type="password" 
            value={formData.oldPassword}
            onChange={(e) => setFormData({...formData, oldPassword: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Nowe hasło:</label>
          <input 
            type="password" 
            value={formData.newPassword}
            onChange={(e) => setFormData({...formData, newPassword: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Powtórz:</label>
          <input 
            type="password" 
            value={formData.confirmPassword}
            onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <button 
          type="submit"
          disabled={loading}
          className={`w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light
            ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {loading ? 'Zmienianie...' : 'Zmień'}
        </button>
      </form>
    </div>
  );
};

export const DashboardScreen = ({ onNavigate }) => {
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

export const TournamentsScreen = ({ onNavigate }) => {
  const [tournaments, setTournaments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTournaments = async () => {
      try {
        const response = await api.get('/tournaments/');
        console.log('API Response.data:', response.data);
        setTournaments(response.data);
      } catch (err) {
        setError('Nie udało się pobrać turniejów');
        setTournaments([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTournaments();
  }, []);

  if (loading) {
    return <div className="text-center">Ładowanie...</div>;
  }

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} />
      <h1 className="text-5xl mb-12 font-light">Turnieje</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="w-full max-w-[80%] space-y-6">
        <div className="grid grid-cols-3 gap-4 text-2xl font-light mb-4">
          <div>Nazwa</div>
          <div>Rozpoczęcie</div>
          <div>Organizator</div>
        </div>
        {tournaments.map((tournament) => (
          <div 
            key={tournament._id}
            className="grid grid-cols-3 gap-4 bg-button-bg p-4 rounded cursor-pointer hover:bg-button-hover transition-colors"
            onClick={() => {
              console.log('Navigating with params:', { tournamentId: tournament._id });
              onNavigate('tournament-tree', { tournamentId: tournament._id });
            }}
          >
            <div className="hover:underline">{tournament.name}</div>
            <div>{new Date(tournament.start_date).toLocaleString()}</div>
            <div>{tournament.creator}</div>
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

export const CreateTournamentScreen = ({ onNavigate }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    game: '',
    startTime: '',
    playerLimit: ''
  });
  // const [games, setGames] = useState([]);
  const [error, setError] = useState('');

  // useEffect(() => {
  //   const fetchGames = async () => {
  //     try {
  //       const response = await api.get('/tournaments/');
  //       setGames(response.data);
  //     } catch (err) {
  //       setError('Nie udało się pobrać listy gier');
  //     }
  //   };

  //   fetchGames();
  // }, []);

  const games = ["Kółko i krzyżyk", "Czwórki", "Warcaby"];

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/tournaments/', formData);
      onNavigate('tournaments');
    } catch (err) {
      setError('Nie udało się utworzyć turnieju');
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-12 font-light">Stwórz turniej</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Nazwa:</label>
          <input 
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Opis:</label>
          <input 
            type="text"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Gra:</label>
          <select 
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            value={formData.game}
            onChange={(e) => setFormData({...formData, game: e.target.value})}
          >
            {games.map(game => (
              // <option key={game.id} value={game.id}>{game.name}</option>
              <option key={game}>{game}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="text-2xl font-light">Czas rozpoczęcia:</label>
          <input 
            type="datetime-local"
            value={formData.startTime}
            onChange={(e) => setFormData({...formData, startTime: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Limit graczy:</label>
          <input 
            type="number"
            value={formData.playerLimit}
            onChange={(e) => setFormData({...formData, playerLimit: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <button 
          type="submit"
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Stwórz
        </button>
      </form>
    </div>
  );
};

export const BotsListScreen = ({ onNavigate }) => {
  const [bots, setBots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBots = async () => {
      try {
        const response = await api.get('/bots/');
        setBots(response.data);
        setLoading(false);
      } catch (err) {
        setError('Nie udało się pobrać botów');
        setLoading(false);
      }
    };

    fetchBots();
  }, []);

  const handleDeleteBot = async (botId, e) => {
    e.stopPropagation();
    try {
      await api.delete(`/bots/${botId}/`);
      setBots(bots.filter(bot => bot.id !== botId));
    } catch (err) {
      setError('Nie udało się usunąć bota');
    }
  };

  if (loading) return <div className="text-center">Ładowanie...</div>;

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} />
      <h1 className="text-5xl mb-12 font-light">Boty</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="w-full max-w-[80%] space-y-6">
        <div className="grid grid-cols-3 gap-4 text-2xl font-light mb-4">
          <div>Nazwa</div>
          <div>Gra</div>
          <div></div>
        </div>
        {bots.map((bot) => (
          <div 
            key={bot.id} 
            className="grid grid-cols-3 gap-4 bg-button-bg p-4 rounded cursor-pointer hover:bg-button-hover transition-colors"
            onClick={() => onNavigate('bot-details', { botId: bot._id })}
          >
            <div className="hover:underline">{bot.name}</div>
            <div>{bot.game}</div>
            <button 
              className="bg-button-hover text-white px-6 py-2 rounded hover:bg-primary-bg justify-self-end"
              onClick={(e) => handleDeleteBot(bot.id, e)}
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
export const AddBotScreen = ({ onNavigate }) => {
  const [formData, setFormData] = useState({
    name: '',
    game: ''
  });
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = React.useRef(null);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        const response = await api.get('/games/');
        setGames(response.data);
        if (response.data.length > 0) {
          setFormData(prev => ({...prev, game: response.data[0]}));
        }
      } catch (err) {
        setError('Nie udało się pobrać listy gier');
      }
    };

    fetchGames();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.name.trim().length < 3 || formData.name.trim().length > 16) {
      setError('Nazwa musi mieć od 3 do 16 znaków');
      return;
    }
    if (!formData.game) {
      setError('Wybierz grę');
      return;
    }
    if (!selectedFile) {
      setError('Proszę wybrać plik');
      return;
    }

    const formDataToSend = new FormData();
    formDataToSend.append('code', selectedFile);
    formDataToSend.append('name', formData.name.trim());
    formDataToSend.append('game_type', formData.game._id);

    setLoading(true);
    try {
      await api.post('/bots/', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      onNavigate('bots');
    } catch (err) {
      console.error('Add bot error:', err);
      setError('Nie udało się dodać bota - ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

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
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Nazwa:</label>
          <input 
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            placeholder="Nazwa twojego bota"
            required
          />
        </div>
        <div>
          <label className="text-2xl font-light">Gra:</label>
          <select 
            value={formData.game}
            onChange={(e) => setFormData({...formData, game: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
            required
          >
            {games.map(game => (
              <option key={game} value={game}>{game.name}</option>
            ))}
          </select>
        </div>

        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept=".py"
          className="hidden"
        />

        <div
          className={`w-full h-48 border-2 border-dashed rounded flex flex-col items-center justify-center cursor-pointer transition-colors
            ${isDragging ? 'border-white bg-button-hover' : 'border-button-bg bg-button-bg hover:bg-button-hover'}
            ${selectedFile ? 'bg-button-hover' : ''}`}
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
          type="submit"
          disabled={loading}
          className={`w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light
            ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {loading ? 'Dodawanie...' : 'Dodaj'}
        </button>
      </form>
    </div>
  );
};

export const BotDetailsScreen = ({ onNavigate, botId }) => {
  const [bot, setBot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBotData = async () => {
      try {
        console.log('Bot id: ' + botId);
        
        const botData = await api.get(`/bots/${botId}/`);
        console.log('Bot data:', botData.data);
        setBot(botData.data);
      } catch (err) {
        console.log('Error:', err);
        setError('Nie udało się pobrać danych bota');
      } finally {
        setLoading(false);
      }
    };

    fetchBotData();
  }, []);

  // const handleDeleteBot = async () => {
  //   try {
  //     await botService.deleteBot(bot.id);
  //     onNavigate('bots');
  //   } catch (err) {
  //     setError('Nie udało się usunąć bota');
  //   }
  // };

  if (loading) return <div className="text-center">Ładowanie...</div>;
  if (!bot) return <div className="text-center">Nie znaleziono bota</div>;

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="bots" />
      <h1 className="text-5xl mb-12 font-light">Bot: {bot.name}</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="w-full max-w-[80%] space-y-8">
        <div className="space-y-4">
          <h2 className="text-3xl font-light mb-6">Statystyki:</h2>
          <div className="text-xl font-light">Liczba gier: {bot.games_played}</div>
          <div className="text-xl font-light">Liczba wygranych: {bot.wins}</div>
          <div className="text-xl font-light">Procent wygranych: {bot.games_played === 0 ? "" : ((bot.wins / bot.games_played) * 100).toFixed(1) + "%"}</div> 
        </div>
        {/* <button 
          onClick={handleDeleteBot}
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Usuń bota
        </button> */}
      </div>
    </div>
  );
};

export const JoinTournamentScreen = ({ onNavigate }) => {
  const [accessCode, setAccessCode] = useState('');
  const [error, setError] = useState('');

  const handleJoin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/tournaments/join/', { accessCode });
      onNavigate('select-bot', { 
        tournamentId: response.data.tournamentId,
        gameType: response.data.gameType 
      });
    } catch (err) {
      setError('Nie udało się dołączyć do turnieju');
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-12 font-light">Dołącz do turnieju</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleJoin} className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Kod dostępu:</label>
          <input 
            type="text" 
            value={accessCode}
            onChange={(e) => setAccessCode(e.target.value)}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <button 
          type="submit"
          className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
        >
          Dołącz
        </button>
      </form>
    </div>
  );
};

export const SelectBotScreen = ({ onNavigate }) => {
  const [tournamentInfo, setTournamentInfo] = useState(null);
  const [availableBots, setAvailableBots] = useState([]);
  const [selectedBotId, setSelectedBotId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const params = new URLSearchParams(window.location.search);
        const tournamentId = params.get('tournamentId');
        const gameType = params.get('gameType');

        const tournamentResponse = await api.get(`/tournaments/${tournamentId}/`);
        setTournamentInfo(tournamentResponse.data);

        const botsResponse = await api.get(`/bots/`, {
          params: { gameType }
        });
        setAvailableBots(botsResponse.data);
        
        if (botsResponse.data.length > 0) {
          setSelectedBotId(botsResponse.data[0].id);
        }
      } catch (err) {
        setError('Nie udało się pobrać danych');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleJoin = async () => {
    if (!selectedBotId) {
      setError('Proszę wybrać bota');
      return;
    }

    try {
      await api.post(`/tournaments/${tournamentInfo.id}/participants/`, {
        botId: selectedBotId
      });
      onNavigate('tournaments');
    } catch (err) {
      setError('Nie udało się dołączyć do turnieju');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen w-screen flex items-center justify-center bg-primary-bg text-white">
        Ładowanie...
      </div>
    );
  }

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="join-tournament" />
      <h1 className="text-5xl mb-12 font-light">
        Dołączasz do turnieju {tournamentInfo?.name}
      </h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <div className="w-full max-w-[80%] space-y-6">
        <div className="text-2xl font-light mb-8">
          Gra: {tournamentInfo?.game}
        </div>
        
        {availableBots.length > 0 ? (
          <>
            <div>
              <label className="text-2xl font-light">Wybierz bota:</label>
              <select 
                value={selectedBotId}
                onChange={(e) => setSelectedBotId(e.target.value)}
                className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
              >
                {availableBots.map(bot => (
                  <option key={bot.id} value={bot.id}>
                    {bot.name}
                  </option>
                ))}
              </select>
            </div>
            <button 
              onClick={handleJoin}
              className="w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
            >
              Dołącz
            </button>
          </>
        ) : (
          <div className="text-xl font-light text-center">
            Nie masz dostępnych botów dla tej gry.
            <button
              onClick={() => onNavigate('add-bot')}
              className="block w-full bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover mt-6 text-xl font-light"
            >
              Dodaj nowego bota
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export const ManageTournamentScreen = ({ onNavigate }) => {
  const [tournament, setTournament] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTournament = async () => {
      try {
        const tournamentId = new URLSearchParams(window.location.search).get('id');
        const data = await api.get(`/tournaments/${tournamentId}/`);
        setTournament(data.data);
      } catch (err) {
        setError('Nie udało się pobrać danych turnieju');
      } finally {
        setLoading(false);
      }
    };

    fetchTournament();
  }, []);

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/tournaments/${tournament.id}/`, tournament);
      onNavigate('tournaments');
    } catch (err) {
      setError('Nie udało się zaktualizować turnieju');
    }
  };

  const handleRemoveParticipant = async (participantId) => {
    try {
      await api.delete(`/tournaments/${tournament.id}/participants/${participantId}/`);
      setTournament({
        ...tournament,
        participants: tournament.participants.filter(p => p.id !== participantId)
      });
    } catch (err) {
      setError('Nie udało się usunąć uczestnika');
    }
  };

  if (loading) return <div className="text-center">Ładowanie...</div>;
  if (!tournament) return <div className="text-center">Nie znaleziono turnieju</div>;

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-12 font-light">Zarządzaj: {tournament.name}</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleUpdate} className="w-full max-w-[80%] space-y-6">
        <div>
          <label className="text-2xl font-light">Nazwa:</label>
          <input 
            type="text"
            value={tournament.name}
            onChange={(e) => setTournament({...tournament, name: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Opis:</label>
          <input 
            type="text"
            value={tournament.description}
            onChange={(e) => setTournament({...tournament, description: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Czas rozpoczęcia:</label>
          <input 
            type="datetime-local"
            value={tournament.startTime}
            onChange={(e) => setTournament({...tournament, startTime: e.target.value})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div>
          <label className="text-2xl font-light">Limit graczy:</label>
          <input 
            type="number"
            value={tournament.playerLimit}
            onChange={(e) => setTournament({...tournament, playerLimit: parseInt(e.target.value)})}
            className="w-full p-4 mt-2 bg-button-bg rounded text-xl font-light"
          />
        </div>
        <div className="space-y-4">
          <label className="text-2xl font-light">Uczestnicy:</label>
          {tournament.participants.map((participant) => (
            <div key={participant.id} className="flex justify-between items-center bg-button-bg p-4 rounded">
              <span className="text-xl font-light">{participant.username}</span>
              <button 
                type="button"
                onClick={() => handleRemoveParticipant(participant.id)}
                className="bg-button-hover px-6 py-2 rounded hover:bg-button-bg"
              >
                Usuń
              </button>
            </div>
          ))}
        </div>
        <div className="flex justify-between mt-8">
          <button 
            type="button"
            onClick={async () => {
              try {
                await api.delete(`/tournaments/${tournament.id}/`);
                onNavigate('tournaments');
              } catch (err) {
                setError('Nie udało się anulować turnieju');
              }
            }}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Anuluj turniej
          </button>
          <button 
            type="button"
            onClick={async () => {
              try {
                await api.post(`/tournaments/${tournament.id}/start/`);
                onNavigate('tournament-tree', { tournamentId: tournament.id });
              } catch (err) {
                setError('Nie udało się rozpocząć turnieju');
              }
            }}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Rozpocznij turniej
          </button>
        </div>
      </form>
    </div>
  );
};

export const TournamentMatchScreen = ({ onNavigate, tournamentId, matchId }) => {
  const [match, setMatch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    const fetchMatch = async () => {
      try {
        console.log('Fetching match with params:', { tournamentId, matchId });
        const response = await api.get(`/tournaments/${tournamentId}/matches/${matchId}/`);
        console.log('Match response:', response);
        setMatch(response.data);
      } catch (err) {
        console.error('Error fetching match:', err);
        setError('Nie udało się pobrać danych meczu');
      } finally {
        setLoading(false);
      }
    };

    console.log("t-id: " + tournamentId + " m-id: " + matchId)

    if (tournamentId && matchId) {
      fetchMatch();
    }
  }, [tournamentId, matchId]);

  const handleRunMatch = async () => {
    setIsRunning(true);
    try {
      await api.put(`/tournaments/${tournamentId}/matches/${matchId}/run/`);
      const response = await api.get(`/tournaments/${tournamentId}/matches/${matchId}/`);
      setMatch(response.data);
    } catch (err) {
      console.error('Error running match:', err);
      setError('Nie udało się uruchomić meczu');
    } finally {
      setIsRunning(false);
    }
  };

  if (loading) return <div className="text-center">Ładowanie...</div>;
  if (!match) return <div className="text-center">Nie znaleziono meczu</div>;

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournament-tree" tournamentId={tournamentId} />
      <h1 className="text-5xl mb-12 font-light">
        Mecz {match.game_num}: {match.players.bot1.name} vs {match.players.bot2.name}
      </h1>
      <div className="w-full max-w-[80%] space-y-6">
        <div className="text-2xl font-light text-center mb-12">
          Stan: {match.winner ? `Zwycięzca: ${match.winner.name}` : 'Mecz w toku'}
        </div>
        
        {!match.winner && (
          <button
            onClick={handleRunMatch}
            disabled={isRunning}
            className="w-full bg-button-bg hover:bg-button-bg/80 disabled:opacity-50 disabled:cursor-not-allowed py-4 px-8 rounded-lg text-xl font-light transition-colors"
          >
            {isRunning ? 'Uruchamianie meczu...' : 'Uruchom mecz'}
          </button>
        )}

        {error && (
          <div className="text-red-500 text-center mb-4">
            {error}
          </div>
        )}

        <h3 className="text-2xl font-light mb-4">Historia ruchów:</h3>
        <div className="h-64 bg-button-bg rounded p-4 overflow-auto">
          {match.moves && match.moves.length > 0 ? (
            <pre className="font-mono text-sm">
              {JSON.stringify(match.moves, null, 2)}
            </pre>
          ) : (
            <div className="text-center">Brak historii ruchów</div>
          )}
        </div>
      </div>
    </div>
  );
};

const TournamentTreeScreen = ({ onNavigate, tournamentId }) => {
  const [tournament, setTournament] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTournamentData = async () => {
      try {
        console.log('Tournament id: ' + tournamentId);
        const tournamentResponse = await api.get(`/tournaments/${tournamentId}/`);
        const tournamentData = tournamentResponse.data;
        const matchesResponse = await api.get(`/tournaments/${tournamentId}/matches/`);
        
        for (let i = 0; i < matchesResponse.data.length; i++) {
          const matchResponse = await api.get(`/tournaments/${tournamentId}/matches/${matchesResponse.data[i]._id}/`);
          matchesResponse.data[i] = matchResponse.data;
        }
        
        const matchesData = matchesResponse.data;
        setTournament(tournamentData);
        setMatches(matchesData);
      } catch (err) {
        console.error('Error fetching tournament:', err);
        setError('Nie udało się pobrać danych turnieju');
      } finally {
        setLoading(false);
      }
    };
    
    fetchTournamentData();
  }, [tournamentId]);

  const transformMatchesToBracketFormat = (matches) => {
    return matches.map(match => ({
      id: match._id,
      name: `Match ${match.game_num}`,
      nextMatchId: null, // will need to be calculated
      tournamentRoundText: `Round ${Math.ceil(match.game_num / 2)}`,
      startTime: match.start_date,
      state: match.winner ? "DONE" : "SCHEDULED",
      participants: [
        {
          id: match.players.bot1._id,
          name: match.players.bot1.name,
          resultText: match.winner?.name === match.players.bot1.name ? "Won" : null,
          isWinner: match.winner?.name === match.players.bot1.name,
          status: match.winner ? "PLAYED" : "NO_SHOW",
        },
        {
          id: match.players.bot2._id,
          name: match.players.bot2.name,
          resultText: match.winner?.name === match.players.bot2.name ? "Won" : null,
          isWinner: match.winner?.name === match.players.bot2.name,
          status: match.winner ? "PLAYED" : "NO_SHOW",
        }
      ]
    }));
  };

  const theme = createTheme({
    textColor: { main: '#ffffff', highlighted: '#ffffff', dark: '#ffffff' },
    matchBackground: { winning: '#2d8654', losing: '#c82333', default: '#1e1e1e' },
    score: {
      background: { winning: '#2d8654', losing: '#c82333', default: '#1e1e1e' },
      text: { winning: '#ffffff', losing: '#ffffff', default: '#ffffff' }
    },
    border: {
      color: '#444444',
      highlightedColor: '#888888'
    },
    roundHeader: { backgroundColor: '#2d2d2d', textColor: '#ffffff' },
    connectorColor: '#444444',
    connectorColorHighlight: '#888888',
    svgBackground: '#151515'
  });

  if (loading) return <div className="text-center">Ładowanie...</div>;
  if (!tournament) return <div className="text-center">Nie znaleziono turnieju</div>;

  const bracketMatches = transformMatchesToBracketFormat(matches);

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-start bg-primary-bg text-white p-8 font-kanit">
      <BackButton onNavigate={onNavigate} to="tournaments" />
      <h1 className="text-5xl mb-4 font-light">Turniej: {tournament.name}</h1>
      <div className="text-2xl font-light mb-2">
        Rozpoczęcie: {new Date(tournament.start_date).toLocaleString()}
      </div>
      <div className="text-2xl font-light mb-12">Kod: {tournament.access_code}</div>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      
      <div className="w-full max-w-[90%] h-[600px]">
        <SingleEliminationBracket
          matches={bracketMatches}
          matchComponent={Match}
          theme={theme}
          options={{
            style: {
              roundHeader: {
                backgroundColor: '#2d2d2d',
                fontColor: '#ffffff',
              },
              connectorColor: '#444444',
              connectorColorHighlight: '#888888'
            }
          }}
          svgWrapper={({ children, ...props }) => (
            <SVGViewer 
              width={window.innerWidth * 0.9}
              height={500}
              {...props}
            >
              {children}
            </SVGViewer>
          )}
          onMatchClick={(match) => {
            onNavigate('tournament-match', { 
              tournamentId: tournamentId, 
              matchId: match.id 
            });
          }}
        />
      </div>

      {tournament.creator === localStorage.getItem('userId') && (
        <div className="flex justify-center mt-12">
          <button
            onClick={() => onNavigate('manage-tournament', { tournamentId: tournament._id })}
            className="bg-button-bg text-white px-12 py-4 rounded hover:bg-button-hover text-xl font-light"
          >
            Zarządzaj
          </button>
        </div>
      )}
    </div>
  );
};


const App = () => {
  const [currentScreen, setCurrentScreen] = useState('login');
  const [screenParams, setScreenParams] = useState({}); 

  const handleNavigation = (screen, params = {}) => {
    setCurrentScreen(screen);
    setScreenParams(params);
  };

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

  React.useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token && !['login', 'register'].includes(currentScreen)) {
      setCurrentScreen('login');
      setScreenParams({});
    }
  }, [currentScreen]);

  const CurrentComponent = screens[currentScreen];
  return <CurrentComponent onNavigate={handleNavigation} {...screenParams} />;
};

export default App;
