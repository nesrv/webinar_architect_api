import strawberry
import typing
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi

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

# HTML для простого GraphQL клиента
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Простой GraphQL клиент</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        textarea { width: 100%; height: 200px; margin-bottom: 10px; }
        button { padding: 8px 16px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        pre { background-color: #f5f5f5; padding: 10px; overflow: auto; }
    </style>
</head>
<body>
    <h1>Простой GraphQL клиент для чата</h1>
    
    <h2>Запрос GraphQL</h2>
    <textarea id="query">
# Примеры запросов:

# Получить все чат-комнаты
query {
  chatRooms {
    id
    name
  }
}

# Получить сообщения из конкретной комнаты
# query {
#   messages(chatRoomId: "room-1") {
#     content
#     sender
#     timestamp
#   }
# }

# Отправить сообщение
# mutation {
#   sendMessage(messageInput: {
#     content: "Привет из GraphQL клиента!",
#     sender: "Пользователь",
#     chatRoom: "room-1"
#   }) {
#     id
#     content
#     timestamp
#   }
# }
</textarea>
    
    <button onclick="executeQuery()">Выполнить запрос</button>
    
    <h2>Результат</h2>
    <pre id="result">Здесь будет результат запроса...</pre>
    
    <script>
        async function executeQuery() {
            const query = document.getElementById('query').value;
            
            try {
                const response = await fetch('/graphql', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query }),
                });
                
                const data = await response.json();
                document.getElementById('result').textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').textContent = 'Ошибка: ' + error.message;
            }
        }
    </script>
</body>
</html>
"""

# HTTP-сервер для обработки GraphQL запросов
class GraphQLHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        if self.path == '/graphql':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                request_data = json.loads(post_data)
                query = request_data.get('query', '')
                variables = request_data.get('variables', None)
                
                result = schema.execute_sync(
                    query,
                    variable_values=variables
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result.data).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

# Запуск сервера
if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, GraphQLHandler)
    print("Запуск GraphQL сервера для чата...")
    print("Откройте http://localhost:8000/ в браузере")
    httpd.serve_forever()