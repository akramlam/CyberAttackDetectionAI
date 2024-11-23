import unittest
from src.data.data_collector import NetworkDataCollector
from scapy.all import IP, TCP

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        self.collector = NetworkDataCollector("Ethernet")
        
    def test_packet_processing(self):
        # Create a mock packet
        packet = IP(src="192.168.1.1", dst="192.168.1.2")/TCP(dport=80)
        self.collector.capture_packet(packet)
        
        df = self.collector.get_dataframe()
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['source_ip'], "192.168.1.1") 