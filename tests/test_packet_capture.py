import unittest
from backend.core.packet_capture import PacketCapture
from unittest.mock import Mock, patch

class TestPacketCapture(unittest.TestCase):
    def setUp(self):
        self.packet_capture = PacketCapture()

    @patch('scapy.all.sniff')
    def test_start_capture(self, mock_sniff):
        self.packet_capture.start()
        self.assertTrue(self.packet_capture.is_running)
        self.assertIsNotNone(self.packet_capture.capture_thread)

    def test_process_packet(self):
        mock_packet = Mock()
        mock_packet.src = '192.168.1.1'
        mock_packet.dst = '192.168.1.2'
        mock_packet.proto = 6
        
        packet_data = self.packet_capture._process_packet(mock_packet)
        self.assertIsNotNone(packet_data)
        self.assertEqual(packet_data['source'], '192.168.1.1') 