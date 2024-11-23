import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from typing import List, Dict
import joblib

class AttackPredictor:
    def __init__(self):
        self.model = self._build_model()
        self.scaler = MinMaxScaler()
        
    def _build_model(self):
        """Build LSTM model for attack prediction"""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(64, return_sequences=True, input_shape=(100, 5)),
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model
        
    def predict_next_attack(self, recent_data: np.ndarray) -> Dict:
        """Predict probability and time of next attack"""
        scaled_data = self.scaler.fit_transform(recent_data)
        prediction = self.model.predict(scaled_data.reshape(1, -1, 5))
        
        return {
            'probability': float(prediction[0][0]),
            'estimated_time': self._calculate_attack_time(prediction[0][0])
        }
        
    def _calculate_attack_time(self, probability: float) -> str:
        """Calculate estimated time until next attack"""
        if probability > 0.8:
            return "IMMINENT (< 1 hour)"
        elif probability > 0.6:
            return "Soon (1-3 hours)"
        elif probability > 0.4:
            return "Medium term (3-12 hours)"
        else:
            return "Long term (> 12 hours)" 