### **Урок: Проектирование баз данных SQL**  
**Длительность:** 1 час  
**Уровень:** Начальный/Средний  
**Формат:** Теория (20 мин) + Практика (35 мин) + Обсуждение (5 мин)  

---

## **1. Теоретическая часть (20 мин)**  
### **1.1 Основные концепции**  
**База данных (БД)** – структурированный набор данных, управляемый СУБД (PostgreSQL, MySQL, SQLite).  

**Ключевые понятия:**  
- **Таблицы (Tables):** Структуры для хранения данных (например, `users`, `orders`).  
- **Схема (Schema):** Логическая структура БД (таблицы, связи, ограничения).  
- **Нормализация:** Процесс устранения избыточности данных.  

### **1.2 Нормальные формы**  
| **Нормальная форма** | **Описание**                                  | **Пример нарушения**                |  
|----------------------|----------------------------------------------|-------------------------------------|  
| **1NF**              | Все атрибуты атомарны                        | Поле `phones` со списком номеров    |  
| **2NF**              | Нет частичных зависимостей от составного PK  | `order_details` с ценой товара      |  
| **3NF**              | Нет транзитивных зависимостей                | `employee` с данными отдела         |  

### **1.3 Типы связей**  
- **Один-к-одному (1:1):** Паспорт → Человек.  
- **Один-ко-многим (1:N):** Автор → Книги.  
- **Многие-ко-многим (N:M):** Студенты → Курсы (через промежуточную таблицу).  

---

## **2. Практическая часть (35 мин)**  
### **2.1 Проектирование БД для интернет-магазина**  
**Требования:**  
- Товары, категории, заказы, пользователи.  
- Возможность оставлять отзывы.  

#### **Шаг 1: Создаем таблицы**  
```sql
-- Пользователи
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Категории товаров
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Товары
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT REFERENCES categories(category_id),
    stock_quantity INT DEFAULT 0
);

-- Заказы
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'cancelled'))
);

-- Состав заказа (N:M между orders и products)
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL  -- Фиксируем цену на момент покупки
);

-- Отзывы
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    product_id INT REFERENCES products(product_id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Шаг 2: Заполняем тестовыми данными**  
```sql
INSERT INTO users (username, email) VALUES 
('alice', 'alice@example.com'),
('bob', 'bob@example.com');

INSERT INTO categories (name) VALUES 
('Электроника'),
('Книги');

INSERT INTO products (name, price, category_id, stock_quantity) VALUES
('Ноутбук', 999.99, 1, 10),
('Python для начинающих', 29.99, 2, 50);
```

#### **Шаг 3: Пишем запросы**  
**Пример 1:** Все товары в категории «Электроника»  
```sql
SELECT p.name, p.price 
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE c.name = 'Электроника';
```

**Пример 2:** Пользователи с незавершенными заказами  
```sql
SELECT u.username, o.order_id
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'pending';
```

---

## **3. Оптимизация и индексы (5 мин)**  
### **3.1 Зачем нужны индексы?**  
Ускоряют поиск, но замедляют вставку/обновление.  

**Создание индекса:**  
```sql
CREATE INDEX idx_products_category ON products(category_id);
```

### **3.2 EXPLAIN для анализа запросов**  
```sql
EXPLAIN ANALYZE SELECT * FROM products WHERE price > 100;
```

---

## **4. Распространенные ошибки**  
1. **Отсутствие индексов** на часто используемых полях (`user_id`, `order_date`).  
2. **Избыточность данных** (дублирование цены товара в `order_items` и `products`).  
3. **Игнорирование транзакций** при сложных операциях.  

---

## **5. Домашнее задание**  
1. Добавьте таблицу `discounts` со связью с товарами.  
2. Напишите запрос для расчета общей выручки за месяц.  
3. Проанализируйте запросы через `EXPLAIN`.  

---

## **6. Полезные ресурсы**  
- [Документация PostgreSQL](https://www.postgresql.org/docs/)  
- [SQL-тренажер](https://sqlzoo.net/)  
- [Книга: «SQL для простых смертных»](https://www.ozon.ru/product/sql-dlya-prostyh-smertnyh-108832024/)  

