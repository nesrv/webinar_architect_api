# Интернет-магазин API

Простой REST API для интернет-магазина на FastAPI.

## Запуск

```bash
python shop.py
```

API будет доступен по адресу: http://127.0.0.1:8000
Документация: http://127.0.0.1:8000/docs

## Endpoints

### Товары
- `GET /products` - получить все товары
- `GET /products/{id}` - получить товар по ID

### Корзина
- `POST /cart` - добавить товар в корзину
- `GET /cart` - просмотр корзины
- `DELETE /cart/{product_id}` - удалить товар из корзины

### Заказы
- `POST /order` - создать заказ из корзины
- `GET /orders` - получить все заказы

## Примеры использования

### 1. Получить все товары
```
GET /products
```

### 2. Добавить товар в корзину
```
POST /cart
{
  "product_id": 1,
  "quantity": 2
}
```

### 3. Создать заказ
```
POST /order
```

## Модели данных

- **Product**: id, name, price, stock
- **CartItem**: product_id, quantity  
- **Order**: id, items, total