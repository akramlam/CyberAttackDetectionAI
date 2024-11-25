import React, { useEffect, useState } from 'react';
import { SystemHealth, Anomaly } from '../types/types';
import { monitoringService, securityService } from '../services/api';
import {
    Box,
    Grid,
    Card,
    CardContent,
    Typography,
    CircularProgress,
    Alert,
} from '@mui/material';

export const Dashboard: React.FC = () => {
    const [health, setHealth] = useState<SystemHealth | null>(null);
    const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setError(null);
                const [healthData, anomaliesData] = await Promise.all([
                    monitoringService.getHealth(),
                    securityService.getAnomalies(),
                ]);
                setHealth(healthData);
                setAnomalies(anomaliesData.anomalies);
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'An error occurred';
                setError(errorMessage);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error}</Alert>;

    return (
        <Box p={3}>
            <Grid container spacing={3}>
                {/* System Health */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                System Health
                            </Typography>
                            {health && (
                                <>
                                    <Alert severity={health.status === 'healthy' ? 'success' : 'error'}>
                                        System Status: {health.status}
                                    </Alert>
                                    <Box mt={2}>
                                        <Typography>
                                            CPU Usage: {health.metrics.cpu_usage}%
                                        </Typography>
                                        <Typography>
                                            Memory Usage: {health.metrics.memory_usage}%
                                        </Typography>
                                    </Box>
                                </>
                            )}
                        </CardContent>
                    </Card>
                </Grid>

                {/* Anomalies */}
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Recent Anomalies
                            </Typography>
                            {anomalies.length > 0 ? (
                                anomalies.map((anomaly, index) => (
                                    <Alert key={index} severity="warning" sx={{ mb: 1 }}>
                                        Anomaly detected from {anomaly.packet.source} to{' '}
                                        {anomaly.packet.destination} (Score: {anomaly.score.toFixed(2)})
                                    </Alert>
                                ))
                            ) : (
                                <Typography color="textSecondary">
                                    No anomalies detected
                                </Typography>
                            )}
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
}; 