from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.core.packet_capture import PacketCapture
from backend.ml_engine.anomaly_detector import AnomalyDetector
from backend.database.init_db import init_database
from backend.core.websocket_manager import WebSocketManager
import logging
from backend.api.routes import monitoring, security, auth
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cybersecurity Detection System")

# Initialize database on startup
@app.on_event("startup")
async def startup_db():
    init_database()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
packet_capture = PacketCapture()
anomaly_detector = AnomalyDetector()

# Initialize WebSocket manager
websocket_manager = WebSocketManager()

# Include routers
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["monitoring"])
app.include_router(security.router, prefix="/api/security", tags=["security"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        packet_capture.start()
        logger.info("System started successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        packet_capture.stop()
        logger.info("System shutdown successfully")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

@app.get("/api/traffic/current")
async def get_current_traffic():
    """Get current traffic statistics"""
    try:
        return packet_capture.get_current_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/anomalies")
async def get_anomalies():
    """Get detected anomalies"""
    try:
        current_packets = packet_capture.packets
        if not current_packets:
            return {"anomalies": []}
            
        anomalies = anomaly_detector.detect(current_packets)
        return {"anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train")
async def train_model():
    """Train the anomaly detection model"""
    try:
        current_packets = packet_capture.packets
        if not current_packets:
            raise HTTPException(status_code=400, detail="No training data available")
            
        anomaly_detector.train(current_packets)
        return {"status": "success", "message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket) 