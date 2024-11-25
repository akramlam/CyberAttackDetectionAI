from sklearn.ensemble import IsolationForest
import numpy as np
from ..models.database_models import NetworkPacket
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

class AnomalyDetector:
    def __init__(self, db_session: Session):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.db = db_session
        self.is_trained = False

    def preprocess_data(self, packets):
        """Convert packet data to features"""
        features = []
        for packet in packets:
            # Extract relevant features
            feature_vector = [
                packet.length,
                hash(packet.source_ip) % 1000,  # Hash IP for numerical representation
                hash(packet.dest_ip) % 1000,
                packet.protocol if packet.protocol else 0
            ]
            features.append(feature_vector)
        return np.array(features)

    def train(self, recent_minutes=30):
        """Train the anomaly detection model"""
        # Get recent packets
        cutoff_time = datetime.now() - timedelta(minutes=recent_minutes)
        recent_packets = self.db.query(NetworkPacket).filter(
            NetworkPacket.timestamp >= cutoff_time
        ).all()

        if not recent_packets:
            return False

        # Preprocess data and train model
        X = self.preprocess_data(recent_packets)
        self.model.fit(X)
        self.is_trained = True
        return True

    def detect_anomalies(self, packets):
        """Detect anomalies in packets"""
        if not self.is_trained:
            return []

        X = self.preprocess_data(packets)
        predictions = self.model.predict(X)
        scores = self.model.score_samples(X)

        anomalies = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:  # Anomaly detected
                anomalies.append({
                    'packet': packets[i],
                    'score': abs(score)
                })

        return anomalies 