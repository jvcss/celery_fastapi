from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # mapeia user_id -> lista de WebSockets
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        connections = self.active_connections.get(user_id, [])
        if websocket in connections:
            connections.remove(websocket)
            if not connections:
                self.active_connections.pop(user_id)

    async def send_personal_message(self, message: str, user_id: int):
        for ws in self.active_connections.get(user_id, []):
            await ws.send_text(message)

    async def broadcast(self, message: str):
        for conns in self.active_connections.values():
            for ws in conns:
                await ws.send_text(message)

# instância única para todo o app
manager = ConnectionManager()