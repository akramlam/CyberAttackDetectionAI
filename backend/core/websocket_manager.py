from fastapi import WebSocket
from typing import List, Dict
import json
import asyncio

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.last_metrics = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Send latest metrics immediately upon connection
        if self.last_metrics:
            await websocket.send_json(self.last_metrics)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_metrics(self, metrics: Dict):
        self.last_metrics = metrics
        for connection in self.active_connections:
            try:
                await connection.send_json(metrics)
            except:
                await self.disconnect(connection)

    async def broadcast_alert(self, alert: Dict):
        for connection in self.active_connections:
            try:
                await connection.send_json({
                    "type": "alert",
                    "data": alert
                })
            except:
                await self.disconnect(connection) 