import React, { useState, useEffect } from 'react';
import {
    Card,
    CardContent,
    Typography,
    List,
    ListItem,
    ListItemText,
    ListItemIcon,
    Chip,
    useTheme
} from '@mui/material';
import {
    Error as ErrorIcon,
    Warning as WarningIcon,
    Info as InfoIcon
} from '@mui/icons-material';
import { notificationService, SecurityEvent } from '../../services/notification';
import { formatDistanceToNow } from 'date-fns';

export const SecurityOverview: React.FC = () => {
    const [events, setEvents] = useState<SecurityEvent[]>([]);
    const theme = useTheme();

    useEffect(() => {
        const unsubscribe = notificationService.addSecurityEventListener((event) => {
            setEvents(prev => [event, ...prev].slice(0, 10)); // Keep last 10 events
        });

        return () => unsubscribe();
    }, []);

    const getIcon = (severity: string) => {
        switch (severity) {
            case 'high':
                return <ErrorIcon color="error" />;
            case 'medium':
                return <WarningIcon color="warning" />;
            default:
                return <InfoIcon color="info" />;
        }
    };

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'high':
                return theme.palette.error.main;
            case 'medium':
                return theme.palette.warning.main;
            default:
                return theme.palette.info.main;
        }
    };

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Security Events
                </Typography>
                <List>
                    {events.map((event) => (
                        <ListItem key={event.id} divider>
                            <ListItemIcon>
                                {getIcon(event.severity)}
                            </ListItemIcon>
                            <ListItemText
                                primary={event.description}
                                secondary={
                                    <>
                                        <Typography component="span" variant="body2">
                                            Source: {event.source_ip} → {event.destination_ip}
                                        </Typography>
                                        <br />
                                        <Typography component="span" variant="body2" color="textSecondary">
                                            {formatDistanceToNow(event.timestamp, { addSuffix: true })}
                                        </Typography>
                                    </>
                                }
                            />
                            <Chip
                                label={event.severity.toUpperCase()}
                                size="small"
                                style={{
                                    backgroundColor: getSeverityColor(event.severity),
                                    color: '#fff'
                                }}
                            />
                        </ListItem>
                    ))}
                </List>
            </CardContent>
        </Card>
    );
}; 