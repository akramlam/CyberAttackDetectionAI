import unittest
from src.web.api import ThreatIntelligence

class TestThreatIntelligence(unittest.TestCase):
    def setUp(self):
        self.threat_intel = ThreatIntelligence()
        
    def test_private_ip(self):
        result = self.threat_intel.check_ip("192.168.1.1")
        self.assertFalse(result['is_malicious'])
        
    def test_malicious_ip(self):
        # Test with known malicious IP
        result = self.threat_intel.check_ip("1.1.1.1")
        self.assertIsInstance(result['threat_score'], float)
        self.assertIsInstance(result['reports'], list) 