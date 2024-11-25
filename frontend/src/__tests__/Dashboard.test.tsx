import React from 'react';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import { act } from '@testing-library/react';
import { Dashboard } from '../components/Dashboard';
import { monitoringService, securityService } from '../services/api';

jest.mock('../services/api', () => ({
    monitoringService: {
        getHealth: jest.fn(),
    },
    securityService: {
        getAnomalies: jest.fn(),
    },
}));

describe('Dashboard Component', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders loading state initially', () => {
        render(<Dashboard />);
        expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    it('displays system health information', async () => {
        const mockHealthData = {
            status: 'healthy',
            metrics: {
                cpu_usage: 25,
                memory_usage: 40,
            },
        };

        const mockAnomaliesData = {
            anomalies: [],
        };

        (monitoringService.getHealth as jest.Mock).mockResolvedValueOnce(mockHealthData);
        (securityService.getAnomalies as jest.Mock).mockResolvedValueOnce(mockAnomaliesData);

        await act(async () => {
            render(<Dashboard />);
        });

        expect(await screen.findByText(/system health/i)).toBeInTheDocument();
        expect(await screen.findByText(/25%/)).toBeInTheDocument();
        expect(await screen.findByText(/40%/)).toBeInTheDocument();
    });

    it('handles error states', async () => {
        const mockError = new Error('Failed to fetch data');
        (monitoringService.getHealth as jest.Mock).mockRejectedValueOnce(mockError);
        (securityService.getAnomalies as jest.Mock).mockResolvedValueOnce({ anomalies: [] });

        await act(async () => {
            render(<Dashboard />);
        });

        expect(await screen.findByText(/failed to fetch data/i)).toBeInTheDocument();
    });
}); 
