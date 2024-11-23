import scapy.all as scapy
from datetime import datetime
import pandas as pd
from typing import List, Dict
import logging
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class NetworkDataCollector:
    def __init__(self, interface: str = "eth0"):
        self.interface = interface
        self.packets: List[Dict] = []
        self.running = False
        
    def capture_packet(self, packet) -> None:
        """Process a single packet and extract relevant features."""
        try:
            if not self.running:
                return
                
            packet_data = {
                'timestamp': datetime.now(),
                'source_ip': packet[scapy.IP].src if packet.haslayer(scapy.IP) else None,
                'dest_ip': packet[scapy.IP].dst if packet.haslayer(scapy.IP) else None,
                'protocol': packet[scapy.IP].proto if packet.haslayer(scapy.IP) else None,
                'length': len(packet),
                'tcp_flags': packet[scapy.TCP].flags if packet.haslayer(scapy.TCP) else None,
                'port': packet[scapy.TCP].dport if packet.haslayer(scapy.TCP) else None
            }
            self.packets.append(packet_data)
        except Exception as e:
            logger.error(f"Error processing packet: {str(e)}")

    def start_capture(self, duration: int = None) -> None:
        """Start capturing network packets."""
        logger.info(f"Starting packet capture on interface {self.interface}")
        self.running = True
        scapy.sniff(iface=self.interface, prn=self.capture_packet, timeout=duration, 
                   stop_filter=lambda _: not self.running)

    def stop_capture(self) -> None:
        """Stop capturing network packets."""
        logger.info("Stopping packet capture")
        self.running = False

    def get_dataframe(self) -> pd.DataFrame:
        """Convert captured packets to pandas DataFrame."""
        return pd.DataFrame(self.packets) 