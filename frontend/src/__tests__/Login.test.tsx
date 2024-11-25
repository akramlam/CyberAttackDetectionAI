import React from 'react';
import '@testing-library/jest-dom';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import { act } from '@testing-library/react';
import { Login } from '../components/Login';
import { AuthProvider } from '../contexts/AuthContext';
import { authService } from '../services/api';

// Mock the auth service
jest.mock('../services/api', () => ({
    authService: {
        login: jest.fn(),
    },
}));

describe('Login Component', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        window.localStorage.clear();
    });

    it('renders login form', () => {
        const { getByLabelText, getByRole } = render(
            <AuthProvider>
                <Login />
            </AuthProvider>
        );

        expect(getByLabelText(/username/i)).toBeInTheDocument();
        expect(getByLabelText(/password/i)).toBeInTheDocument();
        expect(getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    it('handles login submission', async () => {
        const mockLoginResponse = {
            access_token: 'test-token',
            user: {
                id: 1,
                username: 'testuser',
                email: 'test@example.com',
            },
        };

        (authService.login as jest.Mock).mockResolvedValueOnce(mockLoginResponse);

        render(
            <AuthProvider>
                <Login />
            </AuthProvider>
        );

        await act(async () => {
            fireEvent.change(screen.getByLabelText(/username/i), {
                target: { value: 'testuser' },
            });
            fireEvent.change(screen.getByLabelText(/password/i), {
                target: { value: 'password123' },
            });
            fireEvent.click(screen.getByRole('button', { name: /login/i }));
        });

        await waitFor(() => {
            expect(authService.login).toHaveBeenCalledWith('testuser', 'password123');
            expect(window.localStorage.getItem('token')).toBe('test-token');
        });
    });

    it('shows error message on login failure', async () => {
        (authService.login as jest.Mock).mockRejectedValueOnce(new Error('Invalid credentials'));

        render(
            <AuthProvider>
                <Login />
            </AuthProvider>
        );

        await act(async () => {
            fireEvent.change(screen.getByLabelText(/username/i), {
                target: { value: 'testuser' },
            });
            fireEvent.change(screen.getByLabelText(/password/i), {
                target: { value: 'wrongpassword' },
            });
            fireEvent.click(screen.getByRole('button', { name: /login/i }));
        });

        expect(await screen.findByText(/invalid username or password/i)).toBeInTheDocument();
    });
}); 
