import { createContext, useContext } from 'react';

export interface Notification {
    id: string;
    type: 'error' | 'warning' | 'info' | 'success';
    message: string;
    timestamp: Date;
    details?: any;
}

export interface SecurityEvent {
    id: string;
    type: string;
    source_ip: string;
    destination_ip: string;
    severity: 'high' | 'medium' | 'low';
    description: string;
    timestamp: Date;
    anomaly_score?: number;
}

export class NotificationService {
    private listeners: ((notification: Notification) => void)[] = [];
    private eventListeners: ((event: SecurityEvent) => void)[] = [];

    addNotificationListener(listener: (notification: Notification) => void) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }

    addSecurityEventListener(listener: (event: SecurityEvent) => void) {
        this.eventListeners.push(listener);
        return () => {
            this.eventListeners = this.eventListeners.filter(l => l !== listener);
        };
    }

    notify(notification: Notification) {
        this.listeners.forEach(listener => listener(notification));
    }

    notifySecurityEvent(event: SecurityEvent) {
        this.eventListeners.forEach(listener => listener(event));
    }
}

export const notificationService = new NotificationService(); 