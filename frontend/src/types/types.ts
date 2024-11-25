export interface User {
    id: number;
    username: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
}

export interface SystemHealth {
    status: 'healthy' | 'critical';
    metrics: {
        cpu_usage: number;
        memory_usage: number;
        packet_count: number;
        anomaly_count: number;
    };
    alerts: Array<{
        type: string;
        message: string;
    }>;
}

export interface Anomaly {
    packet: {
        timestamp: string;
        source: string;
        destination: string;
        protocol: number;
        length: number;
    };
    score: number;
} 