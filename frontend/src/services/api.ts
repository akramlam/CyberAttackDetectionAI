import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const authService = {
    login: async (username: string, password: string) => {
        const response = await api.post('/auth/token', { username, password });
        return response.data;
    },
    register: async (username: string, email: string, password: string) => {
        const response = await api.post('/auth/register', { username, email, password });
        return response.data;
    },
};

export const monitoringService = {
    getHealth: async () => {
        const response = await api.get('/monitoring/health');
        return response.data;
    },
    getMetrics: async () => {
        const response = await api.get('/monitoring/metrics');
        return response.data;
    },
};

export const securityService = {
    getAnomalies: async () => {
        const response = await api.get('/anomalies');
        return response.data;
    },
    getCurrentTraffic: async () => {
        const response = await api.get('/traffic/current');
        return response.data;
    },
}; 