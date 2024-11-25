from .traffic_generator import TrafficGenerator
from ..services.network_monitor import NetworkMonitorService
from sqlalchemy.orm import Session
import time

class SimulationController:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.traffic_generator = TrafficGenerator()
        self.network_monitor = NetworkMonitorService(db_session)
        
    def start_simulation(self):
        """Start the simulation"""
        print("Starting simulation...")
        
        # Start network monitoring
        self.network_monitor.start_monitoring()
        print("Network monitoring started")
        
        # Start traffic generation
        self.traffic_generator.start()
        print("Traffic generation started")
        
    def stop_simulation(self):
        """Stop the simulation"""
        print("Stopping simulation...")
        
        # Stop traffic generation
        self.traffic_generator.stop()
        print("Traffic generation stopped")
        
        # Stop network monitoring
        self.network_monitor.stop_monitoring()
        print("Network monitoring stopped") 