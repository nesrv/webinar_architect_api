# Интернет-магазин API с SQLite

Интернет-магазин на FastAPI с SQLite базой данных.

## Запуск

```bash
python shop.py
```

API: http://127.0.0.1:8001
Документация: http://127.0.0.1:8001/docs

## Отличия от ex-2

- Данные хранятся в SQLite (`shop.db`)
- Автоматическая инициализация БД
- Персистентное хранение данных
- Порт 8001 (чтобы не конфликтовать с ex-2)

## База данных

### Таблицы:
- `products` - товары (id, name, price, stock)
- `cart` - корзина (id, product_id, quantity)  
- `orders` - заказы (id, items, total)

### Файл БД:
`shop.db` создается автоматически при первом запуске

## API endpoints

Те же что и в ex-2:
- GET /products
- GET /products/{id}
- POST /cart
- GET /cart
- DELETE /cart/{product_id}
- POST /order
- GET /orders