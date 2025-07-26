# Telegram Bot с Webhook

Мини-проект для работы с Telegram Bot API через webhook на FastAPI.

## Настройка

1. Создайте бота через @BotFather в Telegram
2. Замените `YOUR_BOT_TOKEN` в `bot.py` на токен вашего бота
3. Установите зависимости:
```bash
pip install fastapi httpx uvicorn
```

## Запуск

```bash
python bot.py
```

API: http://localhost:8000
Swagger: http://localhost:8000/docs

## Endpoints

### Webhook
- `POST /webhook` - получение сообщений от Telegram
- `POST /set_webhook` - установка webhook URL
- `DELETE /webhook` - удаление webhook

### Сообщения  
- `POST /send` - отправка сообщения
- `GET /messages` - просмотр полученных сообщений

### Информация
- `GET /bot_info` - информация о боте

## Использование

1. Установите webhook:
```json
POST /set_webhook
{
  "webhook_url": "https://your-domain.com/webhook"
}
```

2. Отправьте сообщение:
```json
POST /send
{
  "chat_id": 123456789,
  "text": "Привет!"
}
```

## Примечания

- Для webhook нужен HTTPS URL (используйте ngrok для тестирования)
- Бот автоматически отвечает на входящие сообщения
- Все сообщения сохраняются в памяти