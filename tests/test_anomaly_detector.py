import pytest
from backend.ml_engine.anomaly_detector import AnomalyDetector
import numpy as np

@pytest.fixture
def anomaly_detector():
    return AnomalyDetector()

@pytest.fixture
def sample_data():
    return [
        {
            'length': 100,
            'source': '192.168.1.1',
            'destination': '192.168.1.2',
            'protocol': 6
        },
        {
            'length': 1500,
            'source': '192.168.1.2',
            'destination': '192.168.1.3',
            'protocol': 17
        }
    ]

def test_preprocessing(anomaly_detector, sample_data):
    """Test data preprocessing"""
    processed_data = anomaly_detector.preprocess_data(sample_data)
    assert isinstance(processed_data, np.ndarray)
    assert processed_data.shape[1] == 4  # 4 features

def test_training(anomaly_detector, sample_data):
    """Test model training"""
    anomaly_detector.train(sample_data)
    assert anomaly_detector.is_trained == True

def test_detection(anomaly_detector, sample_data):
    """Test anomaly detection"""
    anomaly_detector.train(sample_data)
    anomalies = anomaly_detector.detect(sample_data)
    assert isinstance(anomalies, list) 