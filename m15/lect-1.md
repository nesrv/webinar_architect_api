### **Урок: Проектирование баз данных NoSQL и DWH**

**Связь с предыдущим уроком:**
Переход от реляционных (SQL) к нереляционным (NoSQL) и хранилищам данных (DWH).
**Длительность:** 1 час
**Уровень:** Средний/Продвинутый
**Формат:** Теория (20 мин) + Практика (35 мин) + Кейсы (5 мин)

---

## **1. Теоретическая часть (20 мин)**

### **1.1 NoSQL vs SQL**

| **Критерий**                 | **SQL**                      | **NoSQL**                                         |
| ------------------------------------------ | ---------------------------------- | ------------------------------------------------------- |
| **Модель данных**        | Таблицы, связи         | Документы/графы/ключ-значение |
| **Схема**                       | Жесткая                     | Гибкая (schemaless)                               |
| **Масштабируемость** | Вертикальная           | Горизонтальная                            |
| **Использование**       | Транзакции, отчеты | Большие данные, IoT                        |

### **1.2 Типы NoSQL БД**

1. **Документные (MongoDB):**
   ```json
   {
     "_id": "user123",
     "name": "Alice",
     "orders": [
       {"product": "Laptop", "price": 999.99}
     ]
   }
   ```
2. **Ключ-значение (Redis):**
   ```bash
   SET user:123:name "Alice"
   GET user:123:name
   ```
3. **Колоночные (Cassandra):** Оптимизированы для аналитики.
4. **Графовые (Neo4j):** Для сложных связей (соцсети, рекомендации).

### **1.3 Data Warehouse (DWH)**

**Отличие от БД:**

- **БД:** Текущие данные, OLTP (Online Transaction Processing).
- **DWH:** Исторические данные, OLAP (Online Analytical Processing).

**Примеры:**

- **PostgreSQL + TimescaleDB** (для временных рядов).
- **Google BigQuery**, **Snowflake** (облачные DWH).

---

## **2. Практическая часть (35 мин)**

### **2.1 Проектирование в MongoDB**

**Задача:** Интернет-магазин с каталогом товаров и отзывами.

#### **Шаг 1: Создаем коллекции**

```javascript
// Подключение к MongoDB (Python)
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["ecommerce"]

// Коллекция "products"
db.products.insert_one({
    "name": "Smartphone",
    "price": 599.99,
    "categories": ["Electronics", "Mobile"],
    "stock": 100,
    "reviews": [
        {"user_id": "user1", "rating": 5, "comment": "Отличный телефон!"}
    ]
})
```

#### **Шаг 2: Запросы**

- **Найти товары дороже 500$:**
  ```javascript
  db.products.find({ "price": { "$gt": 500 } })
  ```
- **Добавить отзыв:**
  ```javascript
  db.products.update_one(
      { "name": "Smartphone" },
      { "$push": { "reviews": {"user_id": "user2", "rating": 4} } }
  )
  ```

---

### **2.2 Проектирование DWH (PostgreSQL + TimescaleDB)**

**Задача:** Анализ продаж за год.

#### **Шаг 1: Создаем гипертаблицу**

```sql
-- Установка TimescaleDB
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Таблица продаж
CREATE TABLE sales (
    time TIMESTAMPTZ NOT NULL,
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2)
);

-- Преобразуем в гипертаблицу
SELECT create_hypertable('sales', 'time');
```

#### **Шаг 2: Аналитические запросы**

- **Продажи по месяцам:**
  ```sql
  SELECT 
      time_bucket('1 month', time) AS month,
      SUM(quantity * price) AS revenue
  FROM sales
  GROUP BY month
  ORDER BY month;
  ```

---

## **3. Кейсы (5 мин)**

### **3.1 Когда выбрать NoSQL?**

- **MongoDB:** Каталог товаров с динамическими атрибутами (например, характеристики телефонов).
- **Redis:** Кэш корзины покупок.
- **Neo4j:** Рекомендательная система ("Купили вместе").

### **3.2 Когда выбрать DWH?**

- **Аналитика продаж** за 5 лет.
- **Прогнозирование** спроса (ML на исторических данных).

---

## **4. Домашнее задание**

1. **Для MongoDB:** Добавьте коллекцию `users` с вложенными заказами.
2. **Для DWH:** Напишите запрос для сравнения продаж по кварталам.
3. **Сравните:** В каких случаях вы выбрали бы SQL, а в каких NoSQL?

---

## **5. Полезные ресурсы**

- [Документация MongoDB](https://www.mongodb.com/docs/)
- [TimescaleDB Tutorial](https://docs.timescale.com/tutorials/)
- [Книга: &#34;NoSQL Distilled&#34;](https://martinfowler.com/books/nosql.html)

🚀 **Итог:** Вы научились проектировать NoSQL-базы и DWH для разных сценариев!
