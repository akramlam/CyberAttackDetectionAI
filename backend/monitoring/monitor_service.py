from datetime import datetime
import psutil
from typing import Dict
from ..models.database_models import SystemMetrics, SecurityEvent
from sqlalchemy.orm import Session
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class MonitoringService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 80.0,
            'anomaly_rate': 0.1,
            'packet_rate': 1000
        }
    
    async def collect_metrics(self) -> Dict:
        try:
            metrics = {
                'timestamp': datetime.utcnow(),
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent,
                'packet_count': 0,
                'anomaly_count': 0,
                'network_io': psutil.net_io_counters()._asdict(),
                'disk_usage': psutil.disk_usage('/').percent
            }
            
            db_metrics = SystemMetrics(**metrics)
            self.db.add(db_metrics)
            self.db.commit()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            raise
            
    async def check_system_health(self) -> Dict:
        """Check system health status"""
        metrics = await self.collect_metrics()
        
        alerts = []
        if metrics['cpu_usage'] > self.alert_thresholds['cpu_usage']:
            alerts.append({
                'type': 'HIGH_CPU',
                'message': f"High CPU usage detected: {metrics['cpu_usage']}%"
            })
            
        if metrics['memory_usage'] > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'HIGH_MEMORY',
                'message': f"High memory usage detected: {metrics['memory_usage']}%"
            })
            
        return {
            'status': 'critical' if alerts else 'healthy',
            'metrics': metrics,
            'alerts': alerts,
            'timestamp': datetime.utcnow().isoformat()
        } 