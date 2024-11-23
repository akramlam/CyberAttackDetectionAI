import unittest
import numpy as np
from src.models.anomaly_detector import AnomalyDetector

class TestAnomalyDetector(unittest.TestCase):
    def setUp(self):
        self.detector = AnomalyDetector(contamination=0.1)
        
    def test_prediction_shape(self):
        X = np.random.rand(100, 5)
        predictions = self.detector.predict(X)
        self.assertEqual(len(predictions), 100)
        
    def test_training_status(self):
        X = np.random.rand(100, 5)
        self.assertFalse(self.detector.is_trained)
        self.detector.train(X)
        self.assertTrue(self.detector.is_trained) 