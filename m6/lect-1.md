### **Практическое занятие: Проектирование API на GraphQL (Python)**  
**Формат:** Теория + Практика с использованием `FastAPI` и `Strawberry`  

---

## **1. Введение **  
### **1.1 Что такое GraphQL?**  
- **GraphQL** – это язык запросов для API, который позволяет клиентам:  
  - Запрашивать только нужные данные (нет over/under-fetching).  
  - Получать несколько ресурсов за один запрос.  
  - Иметь строгую типизацию (схему).  

### **1.2 Отличия от REST**  
| **Критерий**       | **REST**                          | **GraphQL**                     |
|--------------------|-----------------------------------|---------------------------------|
| **Запросы**        | Фиксированные эндпоинты           | Один эндпоинт (`/graphql`)      |
| **Ответ**          | Все поля ресурса                  | Только запрошенные поля         |
| **Типизация**      | Нет (или OpenAPI)                 | Строгая (SDL-схема)             |
| **Версионирование**| Через URL (`/v1/users`)           | Через добавление новых полей    |

---

## **2. Практика: Создаем GraphQL-API (40 минут)**  
### **Задание: API для блога (посты + пользователи)**  
**Стек:**  
- Python 3.10+  
- FastAPI (ASGI-сервер)  
- Strawberry (GraphQL-библиотека)  

#### **Шаг 1: Установка библиотек**  
```bash
pip install fastapi strawberry-graphql uvicorn
```

#### **Шаг 2: Создаем схему GraphQL**  
Файл `schema.py`:  
```python
import strawberry
from typing import List, Optional

# Модели данных
@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author: User  # Связь между типами

# Заглушка для "базы данных"
db = {
    "users": [
        User(id=1, name="Alice", email="alice@example.com"),
        User(id=2, name="Bob", email="bob@example.com"),
    ],
    "posts": [
        Post(id=1, title="Hello", content="Post 1", author=User(id=1, name="Alice", email="alice@example.com")),
        Post(id=2, title="GraphQL", content="Post 2", author=User(id=2, name="Bob", email="bob@example.com")),
    ],
}

# Query (запросы)
@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, id: int) -> Optional[User]:
        return next((u for u in db["users"] if u.id == id), None)

    @strawberry.field
    def get_all_posts(self) -> List[Post]:
        return db["posts"]

# Mutation (изменения)
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_post(self, title: str, content: str, author_id: int) -> Post:
        author = next((u for u in db["users"] if u.id == author_id), None)
        if not author:
            raise ValueError("Author not found")
        
        new_post = Post(
            id=len(db["posts"]) + 1,
            title=title,
            content=content,
            author=author
        )
        db["posts"].append(new_post)
        return new_post

# Создаем схему
schema = strawberry.Schema(query=Query, mutation=Mutation)
```

#### **Шаг 3: Подключаем к FastAPI**  
Файл `main.py`:  
```python
from fastapi import FastAPI
from strawberry.asgi import GraphQL
from schema import schema

app = FastAPI()

# Подключаем GraphQL
app.add_route("/graphql", GraphQL(schema))
app.add_websocket_route("/graphql", GraphQL(schema))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### **Шаг 4: Запуск сервера**  
```bash
python main.py
```
- **GraphQL Playground** будет доступен по адресу: http://localhost:8000/graphql  

---

## **3. Тестирование API (10 минут)**  
### **Примеры запросов**  
1. **Получить все посты с авторами:**  
```graphql
query {
  getAllPosts {
    title
    content
    author {
      name
    }
  }
}
```

2. **Получить конкретного пользователя:**  
```graphql
query {
  getUser(id: 1) {
    name
    email
  }
}
```

3. **Создать новый пост (Mutation):**  
```graphql
mutation {
  createPost(title: "New Post", content: "GraphQL is awesome!", authorId: 1) {
    id
    title
  }
}
```

---

## **4. Плюсы и минусы GraphQL**  
### **✅ Плюсы:**  
- **Гибкость запросов** – клиент выбирает поля.  
- **Экономия трафика** – нет over-fetching.  
- **Строгая типизация** – меньше ошибок.  

### **❌ Минусы:**  
- **Сложность кеширования** – нет стандартных HTTP-кешей.  
- **N+1 проблема** – требует решения (DataLoader).  
- **Кривая обучения** – новичкам сложнее, чем REST.  

---

## **5. Дополнительные задания**  
1. **Добавьте удаление постов** (новое поле в `Mutation`).  
2. **Реализуйте пагинацию** для `getAllPosts`.  
3. **Подключите базу данных** (SQLAlchemy, Django ORM).  

---

## **6. Итоги**  
- GraphQL – мощная альтернатива REST для сложных API.  
- **Strawberry** – одна из лучших GraphQL-библиотек для Python.  
- **Используйте GraphQL, когда:**  
  - Нужна гибкость в запросах.  
  - Много связей между сущностями.  
  - Клиенты мобильные (важен размер ответа).  

**Документация:**  
- [Strawberry](https://strawberry.rocks/)  
- [GraphQL Official](https://graphql.org/)  

