from datetime import datetime
import logging
from typing import Dict, Any
from ..utils.logger import setup_logger
from ..models.database import DatabaseManager
from flask_socketio import emit
from flask import current_app
from ..web.api import ThreatIntelligence
from ..monitoring.response_actions import ResponseActions

logger = setup_logger(__name__)

class AlertSystem:
    def __init__(self, db_manager: DatabaseManager):
        self.alert_levels = {
            0: "INFO",
            1: "WARNING",
            2: "CRITICAL"
        }
        self.db = db_manager
        self.threat_intel = ThreatIntelligence()
        self.response_actions = ResponseActions()
        
    def generate_alert(self, 
                      source_ip: str,
                      alert_level: int,
                      details: Dict[str, Any]) -> None:
        """Generate and log security alerts."""
        timestamp = datetime.now()
        
        # Format alert data for the web interface
        alert_data = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'source_ip': source_ip,
            'level': self.alert_levels[alert_level],
            'details': {
                'features': details.get('features', []),
                'anomaly_score': details.get('anomaly_score', 0.0),
                'timestamp': details.get('timestamp', str(timestamp))
            }
        }
        
        # Log alert
        alert_message = (
            f"[{alert_data['level']}] "
            f"Suspicious activity detected from {source_ip}\n"
            f"Timestamp: {alert_data['timestamp']}\n"
            f"Details: {alert_data['details']}"
        )
        
        if alert_level >= 2:
            logger.critical(alert_message)
        elif alert_level == 1:
            logger.warning(alert_message)
        else:
            logger.info(alert_message)
            
        # Store in database
        event_data = {
            'timestamp': timestamp,
            'source_ip': source_ip,
            'alert_level': alert_level,
            'features': details.get('features'),
            'anomaly_score': details.get('anomaly_score', 0.0)
        }
        self.db.add_event(event_data)
        
        try:
            # Emit websocket event for real-time updates
            if current_app:
                emit('new_alert', alert_data, broadcast=True, namespace='/')
        except Exception as e:
            logger.error(f"Failed to emit alert: {str(e)}")