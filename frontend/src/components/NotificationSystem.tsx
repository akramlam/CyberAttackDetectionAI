import React, { useEffect, useState } from 'react';
import { Snackbar, Alert } from '@mui/material';
import { notificationService, Notification } from '../services/notification';

export const NotificationSystem: React.FC = () => {
    const [notification, setNotification] = useState<Notification | null>(null);
    const [open, setOpen] = useState(false);

    useEffect(() => {
        const unsubscribe = notificationService.addNotificationListener((newNotification) => {
            setNotification(newNotification);
            setOpen(true);
        });

        return () => unsubscribe();
    }, []);

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <Snackbar
            open={open}
            autoHideDuration={6000}
            onClose={handleClose}
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        >
            {notification && (
                <Alert
                    onClose={handleClose}
                    severity={notification.type}
                    variant="filled"
                    elevation={6}
                >
                    {notification.message}
                </Alert>
            )}
        </Snackbar>
    );
}; 