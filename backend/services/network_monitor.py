import threading
from datetime import datetime
from ..core.packet_capture import PacketCapture
from ..ml_engine.anomaly_detector import AnomalyDetector
from ..core.alert_system import AlertSystem
from sqlalchemy.orm import Session

class NetworkMonitorService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.packet_capture = PacketCapture(db_session)
        self.anomaly_detector = AnomalyDetector(db_session)
        self.alert_system = AlertSystem(db_session)
        self.monitoring_thread = None
        self.is_monitoring = False

    def start_monitoring(self):
        """Start network monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.packet_capture.start_capture()
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
            self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop network monitoring"""
        self.is_monitoring = False
        self.packet_capture.stop_capture()
        if self.monitoring_thread:
            self.monitoring_thread.join()

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Train anomaly detector if needed
                if not self.anomaly_detector.is_trained:
                    self.anomaly_detector.train()

                # Get recent packets
                recent_packets = self.db.query(NetworkPacket).order_by(
                    NetworkPacket.timestamp.desc()
                ).limit(1000).all()

                # Detect anomalies
                anomalies = self.anomaly_detector.detect_anomalies(recent_packets)

                # Create alerts for anomalies
                for anomaly in anomalies:
                    self.alert_system.create_alert(
                        alert_type="ANOMALY",
                        severity="HIGH" if anomaly['score'] > 0.8 else "MEDIUM",
                        message=f"Anomalous traffic detected from {anomaly['packet'].source_ip}",
                        details={
                            'score': anomaly['score'],
                            'packet_info': {
                                'source': anomaly['packet'].source_ip,
                                'destination': anomaly['packet'].dest_ip,
                                'protocol': anomaly['packet'].protocol,
                                'length': anomaly['packet'].length
                            }
                        }
                    )

            except Exception as e:
                print(f"Error in monitoring loop: {e}") 