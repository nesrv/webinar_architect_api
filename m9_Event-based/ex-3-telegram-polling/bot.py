from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import httpx
import asyncio
from contextlib import asynccontextmanager

BOT_TOKEN = "YOUR_BOT_TOKEN"  # Замените на токен вашего бота
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

messages = []
polling_task = None
offset = 0

class SendMessage(BaseModel):
    chat_id: int
    text: str

async def polling():
    """Polling для получения сообщений"""
    global offset
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(
                    f"{TELEGRAM_API}/getUpdates",
                    params={"offset": offset, "timeout": 30}
                )
                data = response.json()
                
                if data.get("ok") and data.get("result"):
                    for update in data["result"]:
                        offset = update["update_id"] + 1
                        
                        if "message" in update:
                            message = update["message"]
                            messages.append({
                                "update_id": update["update_id"],
                                "chat_id": message["chat"]["id"],
                                "user": message["from"]["first_name"],
                                "text": message.get("text", ""),
                                "date": message["date"]
                            })
                            
                            # Автоответ
                            chat_id = message["chat"]["id"]
                            response_text = f"Получено: {message.get('text', '')}"
                            await send_telegram_message(chat_id, response_text)
                            
            except Exception as e:
                print(f"Polling error: {e}")
                await asyncio.sleep(5)

async def send_telegram_message(chat_id: int, text: str):
    """Отправка сообщения в Telegram"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text}
        )
        return response.json()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск polling при старте
    global polling_task
    polling_task = asyncio.create_task(polling())
    yield
    # Остановка polling при завершении
    if polling_task:
        polling_task.cancel()

app = FastAPI(title="Telegram Bot Polling API", lifespan=lifespan)

@app.post("/send")
async def send_message(msg: SendMessage):
    """Отправка сообщения через API"""
    result = await send_telegram_message(msg.chat_id, msg.text)
    return result

@app.get("/messages")
def get_messages():
    """Получить все полученные сообщения"""
    return messages

@app.delete("/messages")
def clear_messages():
    """Очистить сообщения"""
    global messages
    messages = []
    return {"ok": True}

@app.get("/bot_info")
async def get_bot_info():
    """Информация о боте"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TELEGRAM_API}/getMe")
        return response.json()

@app.get("/status")
def get_status():
    """Статус polling"""
    return {
        "polling_active": polling_task and not polling_task.done(),
        "messages_count": len(messages),
        "current_offset": offset
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)