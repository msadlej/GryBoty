import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { act } from 'react';
import axios from 'axios';
import App from '../src/App';
import { 
    LoginScreen, 
    RegisterScreen, 
    DashboardScreen, 
    TournamentsScreen,
    CreateTournamentScreen,
    BotsListScreen,
    AddBotScreen,
    SettingsScreen,
    TournamentTreeScreen,
    JoinTournamentScreen,
    SelectBotScreen,
    TournamentMatchScreen,
    ChangePasswordScreen
  } from '../src/App';

jest.mock('axios', () => {
  const mockAxiosInstance = {
    post: jest.fn(),
    get: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
    interceptors: {
      request: { use: jest.fn(), eject: jest.fn() },
      response: { use: jest.fn(), eject: jest.fn() },
    },
  };

  const axios = {
    create: jest.fn(() => mockAxiosInstance),
    post: jest.fn(),
  };

  return {
    __esModule: true,
    default: axios,
  };
});

const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('Authentication Flow', () => {
    beforeEach(() => {
      jest.clearAllMocks();
    });
  
    test('successful login navigates to dashboard', async () => {
      const mockNavigate = jest.fn();
      const mockAxiosInstance = axios.create();
      mockAxiosInstance.post.mockResolvedValueOnce({ data: { access_token: 'test-token' } });
  
      render(<LoginScreen onNavigate={mockNavigate} />);
  
      await act(async () => {
        const inputs = screen.getAllByRole('textbox');
        const passwordInputs = screen.getAllByDisplayValue('').filter(input => input.type === 'password');
  
        fireEvent.change(inputs[0], { target: { value: 'testuser' } });
        fireEvent.change(passwordInputs[0], { target: { value: 'password' } });
        
        const submitButton = screen.getByRole('button', { name: /zaloguj się/i });
        fireEvent.click(submitButton);
      });
  
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('dashboard');
        expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'test-token');
      });
    });
  
    test('displays error message on failed login', async () => {
      const mockNavigate = jest.fn();
      const mockAxiosInstance = axios.create();
      mockAxiosInstance.post.mockRejectedValueOnce(new Error('Login failed'));
  
      render(<LoginScreen onNavigate={mockNavigate} />);
  
      await act(async () => {
        const inputs = screen.getAllByRole('textbox');
        const passwordInputs = screen.getAllByDisplayValue('').filter(input => input.type === 'password');
        
        fireEvent.change(inputs[0], { target: { value: 'testuser' } });
        fireEvent.change(passwordInputs[0], { target: { value: 'wrongpass' } });
        
        const submitButton = screen.getByRole('button', { name: /zaloguj się/i });
        fireEvent.click(submitButton);
      });
  
      await waitFor(() => {
        expect(screen.getByText('Nieprawidłowy login lub hasło')).toBeInTheDocument();
        expect(mockNavigate).not.toHaveBeenCalled();
      });
    });
  
    test('registration with matching passwords works', async () => {
      const mockNavigate = jest.fn();
      const mockAxiosInstance = axios.create();
      mockAxiosInstance.post.mockResolvedValueOnce({ data: { success: true } });
  
      render(<RegisterScreen onNavigate={mockNavigate} />);
  
      await act(async () => {
        const inputs = screen.getAllByRole('textbox');
        const passwordInputs = screen.getAllByDisplayValue('').filter(input => input.type === 'password');
        
        fireEvent.change(inputs[0], { target: { value: 'newuser' } });
        fireEvent.change(passwordInputs[0], { target: { value: 'password123' } });
        fireEvent.change(passwordInputs[1], { target: { value: 'password123' } });
        
        const registerButton = screen.getByRole('button', { name: /zarejestruj/i });
        fireEvent.click(registerButton);
      });
  
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('login');
      });
    });
  
    test('registration with non-matching passwords shows error', async () => {
      const mockNavigate = jest.fn();
      render(<RegisterScreen onNavigate={mockNavigate} />);
  
      await act(async () => {
        const inputs = screen.getAllByRole('textbox');
        const passwordInputs = screen.getAllByDisplayValue('').filter(input => input.type === 'password');
        
        fireEvent.change(inputs[0], { target: { value: 'newuser' } });
        fireEvent.change(passwordInputs[0], { target: { value: 'password123' } });
        fireEvent.change(passwordInputs[1], { target: { value: 'password456' } });
        
        const registerButton = screen.getByRole('button', { name: /zarejestruj/i });
        fireEvent.click(registerButton);
      });
  
      await waitFor(() => {
        expect(screen.getByText('Hasła nie są identyczne')).toBeInTheDocument();
        expect(mockNavigate).not.toHaveBeenCalled();
      });
    });
  
    test('handles registration API error', async () => {
      const mockNavigate = jest.fn();
      const mockAxiosInstance = axios.create();
      mockAxiosInstance.post.mockRejectedValueOnce(new Error('Registration failed'));
  
      render(<RegisterScreen onNavigate={mockNavigate} />);
  
      await act(async () => {
        const inputs = screen.getAllByRole('textbox');
        const passwordInputs = screen.getAllByDisplayValue('').filter(input => input.type === 'password');
        
        fireEvent.change(inputs[0], { target: { value: 'newuser' } });
        fireEvent.change(passwordInputs[0], { target: { value: 'password123' } });
        fireEvent.change(passwordInputs[1], { target: { value: 'password123' } });
        
        const registerButton = screen.getByRole('button', { name: /zarejestruj/i });
        fireEvent.click(registerButton);
      });
  
      await waitFor(() => {
        expect(screen.getByText('Nie udało się zarejestrować użytkownika')).toBeInTheDocument();
      });
    });
  });
  
  describe('Password Management', () => {
    test('change password shows error on mismatch', async () => {
      const mockNavigate = jest.fn();
      render(<ChangePasswordScreen onNavigate={mockNavigate} />);
  
      await act(async () => {
        const inputs = screen.getAllByDisplayValue('').filter(input => input.type === 'password');
        
        fireEvent.change(inputs[0], { target: { value: 'oldpass' } });
        fireEvent.change(inputs[1], { target: { value: 'newpass1' } });
        fireEvent.change(inputs[2], { target: { value: 'newpass2' } });
        
        const submitButton = screen.getByRole('button', { name: /zmień/i });
        fireEvent.click(submitButton);
      });
  
      await waitFor(() => {
        expect(screen.getByText('Nowe hasła nie są identyczne')).toBeInTheDocument();
      });
    });
  });
  
  describe('Tournament Management', () => {
    beforeEach(() => {
      jest.clearAllMocks();
    });
  
    test('tournaments list displays correctly', async () => {
      const mockNavigate = jest.fn();
      const mockAxiosInstance = axios.create();
      const mockTournaments = [
        { _id: '1', name: 'Tournament 1', start_date: '2025-01-15', creator: 'user1' },
        { _id: '2', name: 'Tournament 2', start_date: '2025-01-16', creator: 'user2' }
      ];
  
      mockAxiosInstance.get.mockResolvedValueOnce({ data: mockTournaments });
  
      render(<TournamentsScreen onNavigate={mockNavigate} />);
  
      await waitFor(() => {
        expect(screen.getByText('Tournament 1')).toBeInTheDocument();
        expect(screen.getByText('Tournament 2')).toBeInTheDocument();
      });
  
      const tournamentElement = screen.getByText('Tournament 1');
      fireEvent.click(tournamentElement);
  
      expect(mockNavigate).toHaveBeenCalledWith('tournament-tree', { tournamentId: '1' });
    });
  
    test('create tournament form works correctly', async () => {
      const mockNavigate = jest.fn();
      const mockAxiosInstance = axios.create();
      mockAxiosInstance.post.mockResolvedValueOnce({ data: { success: true } });
  
      render(<CreateTournamentScreen onNavigate={mockNavigate} />);
  
      await act(async () => {
        const inputs = screen.getAllByRole('textbox');
        fireEvent.change(inputs[0], { target: { value: 'New Tournament' } });
        fireEvent.change(inputs[1], { target: { value: 'Description' } });
        
        const numberInput = screen.getByRole('spinbutton');
        fireEvent.change(numberInput, { target: { value: '8' } });
  
        const createButton = screen.getByRole('button', { name: /stwórz/i });
        fireEvent.click(createButton);
      });
  
      await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('tournaments');
      });
    });
  
    test('join tournament with access code', async () => {
        const mockNavigate = jest.fn();
        const mockAxios = axios.create();
        const responseData = { data: { tournamentId: '123', gameType: 'chess' } };
        
        mockAxios.post.mockImplementation(() => Promise.resolve(responseData));
        
        render(<JoinTournamentScreen onNavigate={mockNavigate} />);
    
        await act(async () => {
          const input = screen.getByRole('textbox');
          fireEvent.change(input, { target: { value: 'ABC123' } });
          
          const submitButton = screen.getByRole('button', { name: /dołącz/i });
          await fireEvent.click(submitButton);
        });
    
        await waitFor(() => {
          expect(mockNavigate).toHaveBeenCalledWith('select-bot', {
            tournamentId: responseData.data.tournamentId,
            gameType: responseData.data.gameType
          });
        });
      });
  
    test('tournament match display', async () => {
      const mockNavigate = jest.fn();
      const mockAxiosInstance = axios.create();
      const mockMatch = {
        _id: '1',
        game_num: 1,
        players: { bot1: 'Bot1', bot2: 'Bot2' },
        winner: 'Bot1',
        moves: ['move1', 'move2']
      };
  
      mockAxiosInstance.get.mockResolvedValueOnce({ data: mockMatch });
  
      render(<TournamentMatchScreen 
        onNavigate={mockNavigate}
        tournamentId="123"
        matchId="1"
      />);
  
      await waitFor(() => {
        expect(screen.getByText(/Bot1 vs Bot2/i)).toBeInTheDocument();
        expect(screen.getByText(/Zwycięzca: Bot1/i)).toBeInTheDocument();
      });
    });
  });

describe('Bot Management', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('bots list displays correctly', async () => {
    const mockNavigate = jest.fn();
    const mockAxiosInstance = axios.create();
    const mockBots = [
      { id: '1', name: 'Bot 1', game: 'Game 1' },
      { id: '2', name: 'Bot 2', game: 'Game 2' }
    ];

    mockAxiosInstance.get.mockResolvedValueOnce({ data: mockBots });

    render(<BotsListScreen onNavigate={mockNavigate} />);

    await waitFor(() => {
      expect(screen.getByText('Bot 1')).toBeInTheDocument();
      expect(screen.getByText('Bot 2')).toBeInTheDocument();
    });
  });

  test('add bot form handles file upload', async () => {
    const mockNavigate = jest.fn();
    const mockAxiosInstance = axios.create();
    mockAxiosInstance.post.mockResolvedValueOnce({ data: { success: true } });

    render(<AddBotScreen onNavigate={mockNavigate} />);

    const file = new File(['test content'], 'test.py', { type: 'text/x-python' });

    await act(async () => {
      const fileInput = screen.getByRole('textbox', { hidden: true });
      const nameInput = screen.getByPlaceholderText(/nazwa twojego bota/i);
      const gameSelect = screen.getByRole('combobox');

      Object.defineProperty(fileInput, 'files', { value: [file] });
      fireEvent.change(nameInput, { target: { value: 'New Bot' } });
      fireEvent.change(gameSelect, { target: { value: 'Kółko i krzyżyk' } });
    });
  });
});

describe('Settings Management', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('settings screen displays user info', async () => {
    const mockNavigate = jest.fn();
    const mockAxiosInstance = axios.create();
    mockAxiosInstance.get.mockResolvedValueOnce({ data: { username: 'testuser' } });

    render(<SettingsScreen onNavigate={mockNavigate} />);

    await waitFor(() => {
      expect(screen.getByText(/zalogowany jako: testuser/i)).toBeInTheDocument();
    });

    const logoutButton = screen.getByRole('button', { name: /wyloguj się/i });
    fireEvent.click(logoutButton);

    expect(mockNavigate).toHaveBeenCalledWith('login');
  });
});