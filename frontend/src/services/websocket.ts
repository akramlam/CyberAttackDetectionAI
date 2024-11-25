import { notificationService } from './notification';

export class WebSocketService {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;

    constructor(private url: string) {}

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            switch (data.type) {
                case 'security_event':
                    notificationService.notifySecurityEvent({
                        ...data.payload,
                        timestamp: new Date(data.payload.timestamp)
                    });
                    break;
                    
                case 'alert':
                    notificationService.notify({
                        id: Date.now().toString(),
                        type: data.payload.severity,
                        message: data.payload.message,
                        timestamp: new Date(),
                        details: data.payload
                    });
                    break;
                    
                case 'metrics':
                    // Handle metrics update
                    if (this.onMetricsUpdate) {
                        this.onMetricsUpdate(data.payload);
                    }
                    break;
            }
        };

        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                setTimeout(() => {
                    this.reconnectAttempts++;
                    this.connect();
                }, 1000 * Math.pow(2, this.reconnectAttempts));
            }
        };
    }

    onMetricsUpdate: ((metrics: any) => void) | null = null;

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
}

export const websocketService = new WebSocketService('ws://localhost:8000/ws'); 