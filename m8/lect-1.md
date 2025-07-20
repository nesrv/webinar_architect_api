### ** Проектирование API – REST**  
**Длительность:** 1 час  
**Уровень:** Начальный/Средний  
**Формат:** Теория + Практика на Python (FastAPI)  

---

## **1. Введение **  
### **1.1 Что такое REST?**  
- **REST** (Representational State Transfer) – архитектурный стиль для веб-API.  
- **Ключевые принципы:**  
  - **Ресурсы** (сущности: пользователи, товары).  
  - **HTTP-методы** (GET, POST, PUT, DELETE).  
  - **Статус-коды** (200, 404, 500).  
  - **Без состояния** (каждый запрос независим).  

### **1.2 Сравнение с gRPC/GraphQL**  
| **Критерий**       | **REST**          | **gRPC**            | **GraphQL**         |  
|--------------------|------------------|---------------------|---------------------|  
| **Протокол**       | HTTP/1.1 (JSON)  | HTTP/2 (Protobuf)   | HTTP (JSON)         |  
| **Гибкость**       | Фиксированные эндпоинты | Строгие контракты | Запросы на стороне клиента |  
| **Использование**  | Публичные API    | Микросервисы        | Сложные клиентские приложения |  

### **1.3 Когда выбирать REST?**  
- Публичные API (документация через OpenAPI).  
- Простые CRUD-операции (Create, Read, Update, Delete).  
- Совместимость с браузерами (без дополнительных библиотек).  

---

## **2. Практика: Создание REST-API (35 минут)**  
### **Задание: API для блога (посты и комментарии)**  
**Функционал:**  
- CRUD для постов.  
- Добавление комментариев к посту.  

#### **Шаг 1: Установка FastAPI**  
```bash
pip install fastapi uvicorn
```

#### **Шаг 2: Структура API**  
```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модели данных
class Post(BaseModel):
    id: int
    title: str
    content: str

class Comment(BaseModel):
    id: int
    post_id: int
    text: str

# "База данных"
db = {
    "posts": [
        Post(id=1, title="Первая запись", content="Привет, мир!"),
    ],
    "comments": [
        Comment(id=1, post_id=1, text="Отличный пост!"),
    ],
}
```

#### **Шаг 3: Эндпоинты**  
```python
# Получить все посты
@app.get("/posts", response_model=List[Post])
def get_posts():
    return db["posts"]

# Создать пост
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    db["posts"].append(post)
    return {"message": "Пост создан"}

# Получить комментарии к посту
@app.get("/posts/{post_id}/comments", response_model=List[Comment])
def get_comments(post_id: int):
    return [c for c in db["comments"] if c.post_id == post_id]

# Удалить пост
@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    post = next((p for p in db["posts"] if p.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    db["posts"].remove(post)
    return {"message": "Пост удален"}
```

#### **Шаг 4: Запуск сервера**  
```bash
uvicorn main:app --reload
```
- Документация: http://localhost:8000/docs (Swagger UI).  

---

## **3. Проверка API (10 минут)**  
### **3.1 Примеры запросов**  
1. **Получить все посты:**  
   ```bash
   curl http://localhost:8000/posts
   ```  
2. **Добавить пост:**  
   ```bash
   curl -X POST http://localhost:8000/posts \
     -H "Content-Type: application/json" \
     -d '{"id": 2, "title": "Новый пост", "content": "Еще текст"}'
   ```  
3. **Получить комментарии:**  
   ```bash
   curl http://localhost:8000/posts/1/comments
   ```  

### **3.2 Ответы**  
```json
// GET /posts
[
  {"id": 1, "title": "Первая запись", "content": "Привет, мир!"}
]

// POST /posts
{"message": "Пост создан"}

// GET /posts/1/comments
[
  {"id": 1, "post_id": 1, "text": "Отличный пост!"}
]
```

---

## **4. Критерии качества REST-API**  
1. **Именование ресурсов:**  
   - `/posts` вместо `/getPosts`.  
2. **HTTP-методы:**  
   - GET (чтение), POST (создание), PUT/PATCH (обновление), DELETE (удаление).  
3. **Статус-коды:**  
   - 200 (OK), 201 (Created), 404 (Not Found), 500 (Server Error).  
4. **Версионирование:**  
   - Через URL (`/v1/posts`) или заголовки.  

---

## **5. Дополнительные задания**  
1. **Добавьте пагинацию** для `/posts` (параметры `limit` и `offset`).  
2. **Реализуйте авторизацию** (JWT-токены).  
3. **Подключите базу данных** (SQLite, PostgreSQL).  

---

## **6. Итоги**  
- **REST** – стандарт для публичных API благодаря простоте и поддержке HTTP.  
- **FastAPI** упрощает создание API с автоматической документацией.  
- **Используйте REST, когда:**  
  - Нужна широкая совместимость.  
  - API ориентировано на ресурсы (CRUD).  

**Документация:**  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [REST API Best Practices](https://www.freecodecamp.org/news/rest-api-best-practices/)  

🚀 **Готово!** Вы создали REST-API на Python.