from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import redis
import json
import asyncio

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к Redis для pub/sub
try:
    r = redis.Redis(host='localhost', port=6380, decode_responses=True)
    r.ping()  # Проверка соединения
    print("Успешное подключение к Redis")
    use_redis = True
except (redis.ConnectionError, redis.exceptions.ConnectionError):
    print("Ошибка подключения к Redis. Убедитесь, что Redis запущен.")
    r = None
    use_redis = False

# Сообщения в памяти для режима без Redis
message_history = []

# Хранилище активных соединений
active_connections = set()

# Монтирование статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Настройка шаблонов
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    """Возвращает HTML-страницу чата"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Обработчик WebSocket соединений"""
    await websocket.accept()
    active_connections.add(websocket)
    
    # Сообщение о подключении нового пользователя
    welcome_msg = {"user_id": "System", "text": f"Пользователь {user_id} присоединился к чату"}
    
    # Проверка доступности Redis
    if not use_redis:
        await websocket.send_text("System: Redis недоступен, чат работает в ограниченном режиме")
        # Отправляем сообщение о подключении всем клиентам
        message_history.append(welcome_msg)
        await broadcast_message(f"System: Пользователь {user_id} присоединился к чату")
        
        # Отправляем историю сообщений
        for msg in message_history[-20:]:  # Отправляем последние 20 сообщений
            if "user_id" in msg and "text" in msg:
                await websocket.send_text(f"{msg['user_id']}: {msg['text']}")
    else:
        # Подписка на канал Redis
        pubsub = r.pubsub()
        pubsub.subscribe("chat_channel")
        
        # Отправляем сообщение о подключении в Redis
        r.publish("chat_channel", json.dumps(welcome_msg))

    try:
        while True:
            # Ожидание сообщений от клиента
            data = await websocket.receive_text()
            message = {"user_id": user_id, "text": data}
            
            if use_redis:
                # Публикация в Redis
                r.publish("chat_channel", json.dumps(message))
            else:
                # Сохраняем сообщение в памяти
                message_history.append(message)
                # Ограничиваем историю 100 сообщениями
                if len(message_history) > 100:
                    message_history.pop(0)
                # Отправляем сообщение всем клиентам
                await broadcast_message(f"{user_id}: {data}")
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        
        # Сообщение об отключении пользователя
        leave_msg = {"user_id": "System", "text": f"Пользователь {user_id} покинул чат"}
        
        if use_redis:
            pubsub.unsubscribe("chat_channel")
            r.publish("chat_channel", json.dumps(leave_msg))
        else:
            message_history.append(leave_msg)
            await broadcast_message(f"System: Пользователь {user_id} покинул чат")

async def broadcast_message(message):
    """Отправляет сообщение всем подключенным клиентам"""
    for connection in active_connections.copy():
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            active_connections.remove(connection)

# Фоновый процесс для рассылки сообщений
@app.on_event("startup")
async def startup_event():
    """Запускает фоновую задачу для прослушивания сообщений Redis"""
    if use_redis:
        asyncio.create_task(event_listener())

async def event_listener():
    """Слушает сообщения из Redis и рассылает их всем подключенным клиентам"""
    try:
        pubsub = r.pubsub()
        pubsub.subscribe("chat_channel")
        
        # Создаем асинхронную функцию для обработки сообщений
        while True:
            try:
                message = pubsub.get_message()
                if message and message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        # Сохраняем сообщение в локальной истории
                        message_history.append(data)
                        if len(message_history) > 100:
                            message_history.pop(0)
                            
                        # Рассылка всем подключенным клиентам
                        await broadcast_message(f"{data['user_id']}: {data['text']}")
                    except json.JSONDecodeError as e:
                        print(f"Ошибка декодирования JSON: {e}")
                await asyncio.sleep(0.1)  # Небольшая пауза для снижения нагрузки
            except Exception as e:
                print(f"Ошибка при обработке сообщений Redis: {e}")
                await asyncio.sleep(1)  # Более длительная пауза при ошибке
    except Exception as e:
        print(f"Критическая ошибка в event_listener: {e}")
        global use_redis
        use_redis = False

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)