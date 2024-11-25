import React, { useEffect, useState } from 'react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    ResponsiveContainer
} from 'recharts';
import { Box, Card, CardContent, Typography, Grid, Alert, Snackbar } from '@mui/material';
import { websocketService } from '../../services/websocket';

interface MetricData {
    timestamp: string;
    packetCount: number;
    anomalyScore: number;
}

interface Alert {
    id: number;
    message: string;
    severity: string;
    timestamp: string;
}

export const RealTimeMonitor: React.FC = () => {
    const [metrics, setMetrics] = useState<MetricData[]>([]);
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [showAlert, setShowAlert] = useState(false);
    const [currentAlert, setCurrentAlert] = useState<Alert | null>(null);

    useEffect(() => {
        // Connect to WebSocket
        websocketService.connect();

        // Add listeners
        websocketService.addListener('metrics', (data) => {
            setMetrics(prev => [...prev, data].slice(-30)); // Keep last 30 points
        });

        websocketService.addListener('alert', (alert) => {
            setAlerts(prev => [...prev, alert]);
            setCurrentAlert(alert);
            setShowAlert(true);
        });

        return () => {
            websocketService.disconnect();
        };
    }, []);

    return (
        <Box p={3}>
            {error && <Alert severity="error">{error}</Alert>}
            
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Network Traffic Analysis
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <LineChart data={metrics}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="timestamp" />
                                    <YAxis yAxisId="left" />
                                    <YAxis yAxisId="right" orientation="right" />
                                    <Tooltip />
                                    <Legend />
                                    <Line 
                                        yAxisId="left"
                                        type="monotone"
                                        dataKey="packetCount"
                                        stroke="#8884d8"
                                        name="Packet Count"
                                    />
                                    <Line
                                        yAxisId="right"
                                        type="monotone"
                                        dataKey="anomalyScore"
                                        stroke="#82ca9d"
                                        name="Anomaly Score"
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Recent Alerts
                            </Typography>
                            {alerts.map(alert => (
                                <Alert 
                                    key={alert.id}
                                    severity={alert.severity.toLowerCase() as any}
                                    sx={{ mb: 1 }}
                                >
                                    {alert.message}
                                </Alert>
                            ))}
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            <Snackbar
                open={showAlert}
                autoHideDuration={6000}
                onClose={() => setShowAlert(false)}
            >
                <Alert 
                    severity={currentAlert?.severity.toLowerCase() as any}
                    onClose={() => setShowAlert(false)}
                >
                    {currentAlert?.message}
                </Alert>
            </Snackbar>
        </Box>
    );
}; 