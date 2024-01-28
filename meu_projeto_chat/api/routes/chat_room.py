from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from jose import jwt
from meu_projeto_chat.models.user import User
from meu_projeto_chat.database import get_session


class ChatManager:
    def __init__(self):
        self.rooms = {}

    def get_room(self, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id)
        return self.rooms[room_id]


class ChatRoom:
    def __init__(self, room_id):
        self.room_id = room_id
        self.connections = []

    def connect(self, websocket, user):
        self.connections.append((websocket, user))

    async def broadcast(self, message):
        for connection, user in self.connections:
            await connection.send_text(message)

    def disconnect(self, websocket):
        self.connections = [c for c in self.connections if c[0] != websocket]


async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Substitua a lógica abaixo pela sua lógica real de obtenção do usuário
        user = get_user(username=username)
        return user
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


app = FastAPI()
chat_manager = ChatManager()

router = APIRouter(prefix="/ws", tags=["ws"])


@router.websocket("/ws/{room_id}/{token}")
async def websocket_chatroom(websocket: WebSocket, room_id: str, token: str):
    print("uuu")
    user = await get_current_user(
        token
    )  # Implemente esta função para obter o usuário com base no token JWT
    await websocket.accept()
    room = chat_manager.get_room(room_id)
    room.connect(websocket, user)  # Adiciona o usuário e sua conexão WebSocket à sala

    try:
        while True:
            data = await websocket.receive_text()
            message = (
                f"{user.username}: {data}"  # Prepende o nome do usuário à mensagem
            )
            await room.broadcast(message)  # Transmite a mensagem para todos na sala
    except WebSocketDisconnect:
        room.disconnect(websocket)  # Remove o usuário da sala em caso de desconexão
        await room.broadcast(f"{user.username} left the room {room_id}")
