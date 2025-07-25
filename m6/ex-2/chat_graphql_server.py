from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
import typing
import uuid
from datetime import datetime

# Модели данных
@strawberry.type
class Message:
    id: str
    content: str
    sender: str
    timestamp: str
    chat_room: str

@strawberry.type
class ChatRoom:
    id: str
    name: str
    messages: typing.List[Message]

# Входные типы для мутаций
@strawberry.input
class MessageInput:
    content: str
    sender: str
    chat_room: str

# База данных (имитация)
chat_rooms_db = {}
messages_db = {}

# Инициализация тестовых данных
def initialize_db():
    # Создаем чат-комнаты
    general_id = "room-1"
    support_id = "room-2"
    
    chat_rooms_db[general_id] = {
        "id": general_id,
        "name": "Общий чат",
        "messages": []
    }
    
    chat_rooms_db[support_id] = {
        "id": support_id,
        "name": "Техподдержка",
        "messages": []
    }
    
    # Добавляем сообщения
    message1_id = "msg-1"
    message2_id = "msg-2"
    message3_id = "msg-3"
    
    messages_db[message1_id] = {
        "id": message1_id,
        "content": "Привет всем!",
        "sender": "Иван",
        "timestamp": "2023-05-10 10:15:00",
        "chat_room": general_id
    }
    
    messages_db[message2_id] = {
        "id": message2_id,
        "content": "Как дела?",
        "sender": "Мария",
        "timestamp": "2023-05-10 10:17:30",
        "chat_room": general_id
    }
    
    messages_db[message3_id] = {
        "id": message3_id,
        "content": "У меня проблема с приложением",
        "sender": "Алексей",
        "timestamp": "2023-05-10 11:05:45",
        "chat_room": support_id
    }
    
    # Связываем сообщения с чат-комнатами
    chat_rooms_db[general_id]["messages"] = [message1_id, message2_id]
    chat_rooms_db[support_id]["messages"] = [message3_id]

# Инициализируем базу данных
initialize_db()

# Определение запросов
@strawberry.type
class Query:
    @strawberry.field
    def chat_room(self, id: str) -> typing.Optional[ChatRoom]:
        """Получить информацию о чат-комнате по ID"""
        if id not in chat_rooms_db:
            return None
        
        room_data = chat_rooms_db[id]
        room_messages = []
        
        for msg_id in room_data["messages"]:
            if msg_id in messages_db:
                msg_data = messages_db[msg_id]
                room_messages.append(Message(
                    id=msg_data["id"],
                    content=msg_data["content"],
                    sender=msg_data["sender"],
                    timestamp=msg_data["timestamp"],
                    chat_room=msg_data["chat_room"]
                ))
        
        return ChatRoom(
            id=room_data["id"],
            name=room_data["name"],
            messages=room_messages
        )
    
    @strawberry.field
    def chat_rooms(self) -> typing.List[ChatRoom]:
        """Получить список всех чат-комнат"""
        result = []
        
        for room_id, room_data in chat_rooms_db.items():
            room_messages = []
            
            for msg_id in room_data["messages"]:
                if msg_id in messages_db:
                    msg_data = messages_db[msg_id]
                    room_messages.append(Message(
                        id=msg_data["id"],
                        content=msg_data["content"],
                        sender=msg_data["sender"],
                        timestamp=msg_data["timestamp"],
                        chat_room=msg_data["chat_room"]
                    ))
            
            result.append(ChatRoom(
                id=room_data["id"],
                name=room_data["name"],
                messages=room_messages
            ))
        
        return result
    
    @strawberry.field
    def messages(self, chat_room_id: typing.Optional[str] = None) -> typing.List[Message]:
        """Получить сообщения, опционально фильтруя по чат-комнате"""
        result = []
        
        for msg_id, msg_data in messages_db.items():
            if chat_room_id is None or msg_data["chat_room"] == chat_room_id:
                result.append(Message(
                    id=msg_data["id"],
                    content=msg_data["content"],
                    sender=msg_data["sender"],
                    timestamp=msg_data["timestamp"],
                    chat_room=msg_data["chat_room"]
                ))
        
        # Сортируем сообщения по времени
        result.sort(key=lambda msg: msg.timestamp)
        return result

# Определение мутаций
@strawberry.type
class Mutation:
    @strawberry.mutation
    def send_message(self, message_input: MessageInput) -> typing.Optional[Message]:
        """Отправить новое сообщение"""
        if message_input.chat_room not in chat_rooms_db:
            return None
        
        # Создаем новое сообщение
        message_id = f"msg-{len(messages_db) + 1}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        messages_db[message_id] = {
            "id": message_id,
            "content": message_input.content,
            "sender": message_input.sender,
            "timestamp": timestamp,
            "chat_room": message_input.chat_room
        }
        
        # Добавляем сообщение в чат-комнату
        chat_rooms_db[message_input.chat_room]["messages"].append(message_id)
        
        return Message(
            id=message_id,
            content=message_input.content,
            sender=message_input.sender,
            timestamp=timestamp,
            chat_room=message_input.chat_room
        )
    
    @strawberry.mutation
    def create_chat_room(self, name: str) -> ChatRoom:
        """Создать новую чат-комнату"""
        room_id = f"room-{len(chat_rooms_db) + 1}"
        
        chat_rooms_db[room_id] = {
            "id": room_id,
            "name": name,
            "messages": []
        }
        
        return ChatRoom(
            id=room_id,
            name=name,
            messages=[]
        )

# Создаем схему GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Создаем FastAPI приложение
app = FastAPI()

# Добавляем GraphQL маршрут
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Добавляем корневой маршрут с информацией
@app.get("/")
def read_root():
    return {
        "message": "Простой чат с GraphQL API",
        "graphql_endpoint": "/graphql"
    }

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)