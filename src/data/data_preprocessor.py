import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple
import logging
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract relevant features from raw packet data."""
        features = pd.DataFrame()
        
        # Calculate statistical features
        features['packet_size_mean'] = df.groupby('source_ip')['length'].mean()
        features['packet_count'] = df.groupby('source_ip').size()
        features['unique_ports'] = df.groupby('source_ip')['port'].nunique()
        features['tcp_flags_diversity'] = df.groupby('source_ip')['tcp_flags'].nunique()
        
        # Add time-based features
        features['packets_per_second'] = features['packet_count'] / 60
        
        return features

    def normalize_features(self, features: pd.DataFrame) -> np.ndarray:
        """Normalize features using StandardScaler."""
        return self.scaler.fit_transform(features)

    def prepare_data(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare data for model training/prediction."""
        # Check if dataframe is empty
        if df.empty:
            return np.array([])
        
        features = self.extract_features(df)
        if features.empty:
            return np.array([])
        
        normalized_features = self.normalize_features(features)
        return normalized_features 