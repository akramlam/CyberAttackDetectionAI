import { websocketService } from './websocket';

export interface TrafficData {
    timestamp: Date;
    source_ip: string;
    destination_ip: string;
    protocol: string;
    size: number;
    type: string;
}

class TrafficService {
    private listeners: ((data: TrafficData) => void)[] = [];

    constructor() {
        websocketService.addListener('traffic', (data) => {
            const trafficData: TrafficData = {
                ...data,
                timestamp: new Date(data.timestamp)
            };
            this.notifyListeners(trafficData);
        });
    }

    addListener(callback: (data: TrafficData) => void) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(l => l !== callback);
        };
    }

    private notifyListeners(data: TrafficData) {
        this.listeners.forEach(listener => listener(data));
    }
}

export const trafficService = new TrafficService(); 