from scapy.all import sniff
from datetime import datetime
import threading
from ..models.database_models import NetworkPacket
from sqlalchemy.orm import Session

class PacketCapture:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.is_capturing = False
        self.capture_thread = None

    def start_capture(self):
        """Start packet capture in a separate thread"""
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_packets)
        self.capture_thread.start()

    def stop_capture(self):
        """Stop packet capture"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join()

    def _capture_packets(self):
        """Capture and process network packets"""
        sniff(prn=self._process_packet, store=False, stop_filter=lambda _: not self.is_capturing)

    def _process_packet(self, packet):
        """Process and store captured packet"""
        try:
            packet_data = {
                'timestamp': datetime.now(),
                'source_ip': packet.src if hasattr(packet, 'src') else None,
                'dest_ip': packet.dst if hasattr(packet, 'dst') else None,
                'protocol': packet.proto if hasattr(packet, 'proto') else None,
                'length': len(packet),
                'payload': str(packet.payload) if hasattr(packet, 'payload') else None
            }
            
            network_packet = NetworkPacket(**packet_data)
            self.db.add(network_packet)
            self.db.commit()
            
        except Exception as e:
            print(f"Error processing packet: {e}") 