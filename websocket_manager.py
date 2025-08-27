# websocket_manager.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# Correctly initialize the APIRouter instance
ws_router = APIRouter()

connections = []

@ws_router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    connections.append((username, websocket))
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.remove((username, websocket))

async def notify_user(username: str, message: str):
    for user, ws in connections:
        if user == username:
            await ws.send_text(message)