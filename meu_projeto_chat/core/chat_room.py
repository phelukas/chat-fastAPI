from fastapi import WebSocket


class ChatRoom:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.connections: List[WebSocket] = []

    def connect(self, websocket: WebSocket):
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)
