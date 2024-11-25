from typing import Dict, List
import hashlib
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session
from ..models.database_models import SecurityEvent
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class SecurityService:
    def __init__(self, db_session: Session, secret_key: str):
        self.db = db_session
        self.secret_key = secret_key
        
    def generate_event_signature(self, event_data: Dict) -> str:
        event_string = f"{event_data['timestamp']}{event_data['source_ip']}{event_data['details']}"
        return hashlib.sha256(event_string.encode()).hexdigest()
        
    def log_security_event(self, event_data: Dict) -> None:
        try:
            event = SecurityEvent(
                timestamp=datetime.utcnow(),
                event_type=event_data['type'],
                source_ip=event_data['source_ip'],
                destination_ip=event_data.get('destination_ip'),
                severity=event_data['severity'],
                details=event_data['details'],
                is_anomaly=event_data.get('is_anomaly', False),
                anomaly_score=event_data.get('anomaly_score', 0.0)
            )
            
            self.db.add(event)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
            raise

    def get_security_events(self) -> List[SecurityEvent]:
        """Get all security events"""
        try:
            return self.db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).all()
        except Exception as e:
            logger.error(f"Error retrieving security events: {e}")
            raise

    def generate_token(self, data: Dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> Dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.JWTError:
            raise ValueError("Invalid token")