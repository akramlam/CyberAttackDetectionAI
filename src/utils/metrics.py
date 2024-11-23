from typing import Dict, List
import numpy as np
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.metrics: Dict[str, List] = {
            'processing_time': [],
            'packets_processed': [],
            'alerts_generated': [],
            'anomaly_scores': []
        }
        
    def add_metric(self, metric_name: str, value: float) -> None:
        if metric_name in self.metrics:
            self.metrics[metric_name].append({
                'timestamp': datetime.now(),
                'value': value
            })
            
    def get_average(self, metric_name: str) -> float:
        if metric_name in self.metrics:
            values = [m['value'] for m in self.metrics[metric_name]]
            return np.mean(values) if values else 0
        return 0 