# Интернет-магазин с Redis

Интернет-магазин на FastAPI с Redis в качестве хранилища данных.

## Требования

```bash
pip install fastapi redis uvicorn
```

## Запуск Redis

```bash
# Docker
docker run -d -p 6379:6379 redis:alpine

# Или локально
redis-server
```

## Запуск API

```bash
python shop.py
```

API: http://127.0.0.1:8000

## Структура данных в Redis

- `products` - hash с товарами
- `cart` - hash с корзиной  
- `orders` - hash с заказами
- `order_counter` - счетчик заказов

## Особенности Redis версии

- Быстрое in-memory хранилище
- Автоматическая инициализация данных
- Использование Redis hash для структурированных данных
- Атомарные операции для счетчиков