from datetime import datetime
from sqlalchemy.orm import Session
from ..models.database_models import Alert
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AlertSystem:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_alert(self, alert_type: str, severity: str, message: str, details: dict = None):
        """Create a new alert"""
        try:
            alert = Alert(
                timestamp=datetime.now(),
                alert_type=alert_type,
                severity=severity,
                message=message,
                details=details
            )
            self.db.add(alert)
            self.db.commit()
            logger.info(f"Alert created: {message}")
            return alert
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            raise

    def get_active_alerts(self):
        """Get all active alerts"""
        return self.db.query(Alert).filter(Alert.resolved == False).all()

    def resolve_alert(self, alert_id: int):
        """Mark an alert as resolved"""
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        if alert:
            alert.resolved = True
            alert.resolved_at = datetime.now()
            self.db.commit()
            logger.info(f"Alert {alert_id} resolved")
            return True
        return False 