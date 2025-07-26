from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import asyncio
from typing import List, Dict, Set

# Создаем FastAPI приложение
app = FastAPI()

# Хранилище активных соединений
active_connections: Set[WebSocket] = set()

# Хранилище сообщений в памяти
message_history: List[Dict] = []

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
    # Принимаем соединение
    await websocket.accept()
    
    # Добавляем соединение в список активных
    active_connections.add(websocket)
    
    # Сообщение о подключении нового пользователя
    welcome_msg = {"user_id": "System", "text": f"Пользователь {user_id} присоединился к чату"}
    message_history.append(welcome_msg)
    
    # Отправляем сообщение всем клиентам
    await broadcast_message(f"System: Пользователь {user_id} присоединился к чату")
    
    # Отправляем историю сообщений новому пользователю
    for msg in message_history[-20:]:  # Отправляем последние 20 сообщений
        if "user_id" in msg and "text" in msg:
            await websocket.send_text(f"{msg['user_id']}: {msg['text']}")
    
    try:
        # Бесконечный цикл для получения сообщений от клиента
        while True:
            # Ожидаем сообщение от клиента
            data = await websocket.receive_text()
            
            # Создаем объект сообщения
            message = {"user_id": user_id, "text": data}
            
            # Сохраняем сообщение в истории
            message_history.append(message)
            
            # Ограничиваем историю 100 сообщениями
            if len(message_history) > 100:
                message_history.pop(0)
            
            # Отправляем сообщение всем клиентам
            await broadcast_message(f"{user_id}: {data}")
            
    except WebSocketDisconnect:
        # Удаляем соединение из списка активных
        active_connections.remove(websocket)
        
        # Сообщение об отключении пользователя
        leave_msg = {"user_id": "System", "text": f"Пользователь {user_id} покинул чат"}
        message_history.append(leave_msg)
        
        # Отправляем сообщение всем клиентам
        await broadcast_message(f"System: Пользователь {user_id} покинул чат")

async def broadcast_message(message: str):
    """Отправляет сообщение всем подключенным клиентам"""
    # Перебираем все активные соединения
    for connection in active_connections.copy():
        try:
            # Отправляем сообщение
            await connection.send_text(message)
        except Exception as e:
            # Если возникла ошибка, удаляем соединение из списка активных
            print(f"Ошибка отправки сообщения: {e}")
            active_connections.remove(connection)

if __name__ == "__main__":
    # Запуск сервера
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)