# Telegram Bot с Polling

Мини-проект для работы с Telegram Bot API через long polling на FastAPI.

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

### Сообщения
- `POST /send` - отправка сообщения
- `GET /messages` - просмотр полученных сообщений
- `DELETE /messages` - очистка сообщений

### Информация
- `GET /bot_info` - информация о боте
- `GET /status` - статус polling

## Особенности Polling

- Автоматический запуск при старте сервера
- Long polling с timeout 30 сек
- Автоматическое обновление offset
- Обработка ошибок с повтором через 5 сек
- Автоответ на входящие сообщения

## Использование

1. Отправьте сообщение:
```json
POST /send
{
  "chat_id": 123456789,
  "text": "Привет!"
}
```

2. Просмотрите полученные сообщения:
```
GET /messages
```

## Преимущества Polling

- Не требует HTTPS
- Работает за NAT/firewall
- Простая настройка
- Надежное получение сообщений