import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from progress_manager import ProgressManager

app = FastAPI()

progress_manager = ProgressManager()


@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    await progress_manager.connect(websocket)
    try:
        while True:
            # Wait for messages, but don't require any
            await websocket.receive_text()
    except WebSocketDisconnect:
        progress_manager.disconnect(websocket)


async def update_progress(task_id: str, progress: float):
    """Update progress for a specific task"""
    await progress_manager.broadcast_progress(task_id, progress)


# Example task that reports progress
async def long_running_task(task_id: str):
    for i in range(101):
        await update_progress(task_id, i)
        await asyncio.sleep(0.1)  # Simulate work
