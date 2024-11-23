import numpy as np
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict
import joblib
import logging
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ModelTrainer:
    def __init__(self, model_config: Dict):
        self.model_path = model_config.get('model_path')
        self.retrain_threshold = model_config.get('retrain_threshold', 1000)
        self.samples_since_retrain = 0
        
    def should_retrain(self, new_samples: int) -> bool:
        """Check if model should be retrained"""
        self.samples_since_retrain += new_samples
        return self.samples_since_retrain >= self.retrain_threshold
        
    def retrain_model(self, model, X: np.ndarray) -> Tuple[float, float]:
        """Retrain model with new data"""
        logger.info("Starting model retraining...")
        
        try:
            # Split data for validation
            X_train, X_val = train_test_split(X, test_size=0.2, random_state=42)
            
            # Train model
            model.fit(X_train)
            
            # Evaluate performance
            train_score = model.score_samples(X_train).mean()
            val_score = model.score_samples(X_val).mean()
            
            # Save model
            joblib.dump(model, self.model_path)
            
            self.samples_since_retrain = 0
            logger.info("Model retraining completed successfully")
            
            return train_score, val_score
            
        except Exception as e:
            logger.error(f"Model retraining failed: {str(e)}")
            return None, None 