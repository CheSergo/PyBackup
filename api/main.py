import asyncio
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from progress_manager import ProgressManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

progress_manager = ProgressManager()

@app.websocket("/ws")
async def websocket_progress(websocket: WebSocket):
    print("Новое WebSocket подключение")
    await websocket.accept()
    print("WebSocket соединение установлено")

@app.websocket("/ws/progress")
async def websocket_progress(websocket: WebSocket):
    print("Here")
    await progress_manager.connect(websocket)
    
    # Создаем задачу для периодического обновления
    async def send_periodic_updates():
        task_id = str(uuid.uuid4())  # Уникальный ID для этой сессии
        progress = 0
        
        while True:
            # Обновляем и отправляем прогресс каждую секунду
            progress = (progress + 1) % 101  # Циклический прогресс от 0 до 100
            await progress_manager.broadcast_progress(task_id, progress)
            
            # Ждем секунду перед следующим обновлением
            await asyncio.sleep(2)
    
    # Запускаем задачу в фоновом режиме
    periodic_task = asyncio.create_task(send_periodic_updates())
    
    try:
        while True:
            # Wait for messages, but don't require any
            await websocket.receive_text()
    except WebSocketDisconnect:
        # При отключении клиента завершаем задачу обновлений
        periodic_task.cancel()
        try:
            await periodic_task
        except asyncio.CancelledError:
            pass
        progress_manager.disconnect(websocket)

# @app.websocket("/ws/progress")
# async def websocket_progress(websocket: WebSocket):
#     await progress_manager.connect(websocket)
#     try:
#         while True:
#             # Wait for messages, but don't require any
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         progress_manager.disconnect(websocket)


async def update_progress(task_id: str, progress: float):
    """Update progress for a specific task"""
    await progress_manager.broadcast_progress(task_id, progress)


# Example task that reports progress
async def long_running_task(task_id: str):
    for i in range(101):
        await update_progress(task_id, i)
        await asyncio.sleep(0.1)  # Simulate work

@app.get("/")
async def home():
    return {"Hello" : "World!"}