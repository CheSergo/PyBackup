import json
from typing import Dict, List

from fastapi import WebSocket


class ProgressManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.progress_data: Dict[str, float] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_progress(self, task_id: str, progress: float):
        """Broadcast progress to all connected clients"""
        if progress < 0 or progress > 100:
            raise ValueError("Progress must be between 0 and 100")

        self.progress_data[task_id] = progress
        message = json.dumps({"task_id": task_id, "progress": progress})

        for connection in self.active_connections:
            await connection.send_text(message)
