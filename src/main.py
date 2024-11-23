from src.data.data_collector import NetworkDataCollector
from src.data.data_preprocessor import DataPreprocessor
from src.models.anomaly_detector import AnomalyDetector
from src.monitoring.alert_system import AlertSystem
from src.utils.config import Config
import logging
from src.utils.logger import setup_logger
import time
from src.web.app import app, socketio, dash_app
from src.models.database import DatabaseManager
from src.web.system_monitor import system_bp
from src.utils.report_generator import ReportGenerator
from src.web.control_routes import control_bp, system_running
import threading

logger = setup_logger(__name__)

class IntrusionDetectionSystem:
    def __init__(self, config_path: str):
        self.config = Config(config_path)
        self.db = DatabaseManager(
            self.config.get('database').get('connection_string')
        )
        self.collector = NetworkDataCollector(
            interface=self.config.get('network_interface')
        )
        self.preprocessor = DataPreprocessor()
        self.detector = AnomalyDetector(
            contamination=self.config.get('anomaly_detection').get('contamination')
        )
        self.alert_system = AlertSystem(self.db)
        self.report_generator = ReportGenerator()
        
        # Register blueprints
        app.register_blueprint(system_bp)
        app.register_blueprint(control_bp)
        
    def monitoring_loop(self):
        """Run the monitoring loop in a separate thread."""
        logger.info("Starting monitoring loop...")
        
        while True:
            try:
                # Only process if system is running
                if system_running.is_set():
                    # Collect network data
                    self.collector.start_capture(
                        duration=self.config.get('capture_duration')
                    )
                    
                    # Process data
                    df = self.collector.get_dataframe()
                    if len(df) == 0:
                        continue
                        
                    features = self.preprocessor.prepare_data(df)
                    predictions = self.detector.predict(features)
                    
                    # Generate alerts for anomalies
                    for idx, is_anomaly in enumerate(predictions):
                        if is_anomaly:
                            source_ip = df.iloc[idx]['source_ip']
                            self.alert_system.generate_alert(
                                source_ip=source_ip,
                                alert_level=2,
                                details={
                                    'features': features[idx].tolist(),
                                    'timestamp': str(df.iloc[idx]['timestamp'])
                                }
                            )
                    
                    # Clear captured packets
                    self.collector.packets.clear()
                else:
                    # Sleep when system is stopped
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(5)

    def run(self):
        """Run the IDS system."""
        logger.info("Starting Intrusion Detection System...")
        
        try:
            # Start monitoring in a separate thread
            monitoring_thread = threading.Thread(target=self.monitoring_loop)
            monitoring_thread.daemon = True
            monitoring_thread.start()
            
            # Start the web server in the main thread
            web_config = self.config.get('web_interface')
            socketio.run(
                app, 
                host=web_config.get('host', '0.0.0.0'),
                port=web_config.get('port', 5000),
                debug=False,  # Set to False in production
                use_reloader=False  # Important: disable reloader
            )
            
        except KeyboardInterrupt:
            logger.info("Shutting down IDS gracefully...")
            self.collector.stop_capture()
            logger.info("IDS shutdown complete")

if __name__ == "__main__":
    ids = IntrusionDetectionSystem("config/config.yaml")
    ids.run() 