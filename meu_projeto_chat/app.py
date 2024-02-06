from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import  RedirectResponse

from meu_projeto_chat.api.routes import auth_routes, user_routes

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user_routes.router)
app.include_router(auth_routes.router)


@app.get('/')
def read_root():
    return RedirectResponse(url='/docs')


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str, user_id: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append((websocket, user_id))

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room] = [
                (ws, user_id) for ws, user_id in self.active_connections[room] if ws != websocket
            ]
            if not self.active_connections[room]:
                del self.active_connections[room]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room: str, sender_id: str):
        if room in self.active_connections:
            for connection, user_id in self.active_connections[room]:
                if user_id != sender_id:  
                    await connection.send_text(f"{sender_id}: {message}")



manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    user_id, room = client_id.split('|')  
    print(user_id, room)
    await manager.connect(websocket, room, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"{user_id}: {data}", websocket)
            await manager.broadcast(f"{data}", room, user_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(f"{user_id} left the chat", room, "Server")
