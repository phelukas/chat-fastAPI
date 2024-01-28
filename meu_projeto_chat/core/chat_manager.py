from meu_projeto_chat.core.chat_room import ChatRoom


class ChatManager:
    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}

    def get_room(self, room_id: str) -> ChatRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id)
        return self.rooms[room_id]
