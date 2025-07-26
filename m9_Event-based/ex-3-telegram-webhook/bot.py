from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import asyncio

app = FastAPI(title="Telegram Bot API")

BOT_TOKEN = "YOUR_BOT_TOKEN"  # Замените на токен вашего бота
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

class SendMessage(BaseModel):
    chat_id: int
    text: str

class WebhookUpdate(BaseModel):
    update_id: int
    message: dict = None

# Хранилище сообщений
messages = []

@app.post("/webhook")
async def webhook(update: dict):
    """Получение сообщений от Telegram через webhook"""
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
    
    return {"ok": True}

@app.post("/send")
async def send_message(msg: SendMessage):
    """Отправка сообщения через API"""
    result = await send_telegram_message(msg.chat_id, msg.text)
    return result

@app.get("/messages")
def get_messages():
    """Получить все полученные сообщения"""
    return messages

@app.post("/set_webhook")
async def set_webhook(webhook_url: str):
    """Установить webhook URL"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TELEGRAM_API}/setWebhook",
            json={"url": webhook_url}
        )
        return response.json()

@app.delete("/webhook")
async def delete_webhook():
    """Удалить webhook"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{TELEGRAM_API}/deleteWebhook")
        return response.json()

@app.get("/bot_info")
async def get_bot_info():
    """Информация о боте"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TELEGRAM_API}/getMe")
        return response.json()

async def send_telegram_message(chat_id: int, text: str):
    """Отправка сообщения в Telegram"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text}
        )
        return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)