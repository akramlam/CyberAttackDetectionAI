import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.session import SessionLocal
from backend.simulation.controller import SimulationController
import time

def run_simulation():
    db = SessionLocal()
    try:
        controller = SimulationController(db)
        
        print("=== Cyber Attack Detection Simulation ===")
        print("Starting simulation in 3 seconds...")
        time.sleep(3)
        
        # Start simulation
        controller.start_simulation()
        
        print("\nSimulation is running. Press Ctrl+C to stop.")
        
        # Keep the simulation running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping simulation...")
            controller.stop_simulation()
            print("Simulation stopped.")
            
    finally:
        db.close()

if __name__ == "__main__":
    run_simulation() 