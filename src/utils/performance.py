import psutil
import time
from typing import Dict

class SystemMonitor:
    @staticmethod
    def get_system_metrics() -> Dict:
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict()
        } 