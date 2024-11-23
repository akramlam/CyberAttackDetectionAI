from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
from typing import Tuple
import logging
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AnomalyDetector:
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.is_trained = False
        
    def train(self, X: np.ndarray) -> None:
        """Train the anomaly detection model."""
        logger.info("Training anomaly detection model...")
        self.model.fit(X)
        self.is_trained = True
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict anomalies in the data."""
        if not self.is_trained:
            # Train on the first batch of data
            self.train(X)
            return np.zeros(X.shape[0])  # Return all normal for first batch
            
        predictions = self.model.predict(X)
        # Convert predictions to binary (1 for normal, 0 for anomaly)
        return np.where(predictions == 1, 0, 1)
    
    def save_model(self, path: str) -> None:
        """Save the trained model to disk."""
        joblib.dump(self.model, path)
        
    def load_model(self, path: str) -> None:
        """Load a trained model from disk."""
        self.model = joblib.load(path)
        self.is_trained = True 