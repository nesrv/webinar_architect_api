### **Проектирование API – GraphQL**

**Формат:** Теория + Практика с использованием `FastAPI` и `Strawberry`

---

## **1. Введение в GraphQL**

### **1.1 История и мотивация**

- **Создан Facebook в 2012 году** для решения проблем мобильных приложений
- **Open Source с 2015 года**
- **Проблемы REST**, которые решает GraphQL:
  - **Over-fetching** – получение лишних данных
  - **Under-fetching** – необходимость множественных запросов
  - **Жесткая структура** эндпоинтов
  - **Версионирование API**

### **1.2 Что такое GraphQL?**

**GraphQL** – это:

- **Язык запросов** для API
- **Система типов** для описания данных
- **Исполняющая среда** для выполнения запросов
- **Спецификация**, а не конкретная реализация

**Ключевые принципы:**

- **Один эндпоинт** – `/graphql`
- **Клиент определяет структуру ответа**
- **Строгая типизация**
- **Интроспекция** – API самодокументируется

### **1.3 Архитектура GraphQL**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │───▶│  GraphQL  │───▶│  Resolvers  │
│             │    │   Server    │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Schema    │    │ Data Sources│
                   │   (SDL)     │    │ (DB, API)   │
                   └─────────────┘    └─────────────┘
```

### **1.4 Основные концепции**

#### **Schema Definition Language (SDL)**

```graphql
type User {
  id: ID!
  name: String!
  email: String
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  user(id: ID!): User
  posts: [Post!]!
}

type Mutation {
  createPost(input: CreatePostInput!): Post!
}

type Subscription {
  postAdded: Post!
}
```

#### **Resolvers (Резолверы)**

- **Функции**, которые получают данные для каждого поля
- **Выполняются только для запрошенных полей**
- **Могут быть асинхронными**

---

## **2. Типы данных в GraphQL**

### **2.1 Скалярные типы**

| **Тип** | **Описание**                      | **Пример** |
| ---------------- | ----------------------------------------------- | ---------------------- |
| `String`       | Строка UTF-8                              | `"Hello World"`      |
| `Int`          | 32-битное целое                      | `42`                 |
| `Float`        | Число с плавающей точкой   | `3.14`               |
| `Boolean`      | Логический тип                     | `true`, `false`    |
| `ID`           | Уникальный идентификатор | `"user_123"`         |

### **2.2 Пользовательские скаляры**

```graphql
scalar DateTime
scalar Email
scalar URL

type User {
  id: ID!
  email: Email!
  createdAt: DateTime!
  website: URL
}
```

### **2.3 Объектные типы**

```graphql
type User {
  id: ID!
  name: String!
  profile: UserProfile
}

type UserProfile {
  bio: String
  avatar: String
  location: String
}
```

### **2.4 Списки и Non-Null**

```graphql
type User {
  id: ID!              # Обязательное поле
  name: String         # Опциональное поле
  tags: [String!]      # Список строк (может быть null, но элементы не null)
  posts: [Post!]!      # Обязательный список обязательных постов
}
```

### **2.5 Перечисления (Enums)**

```graphql
enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

type Post {
  id: ID!
  title: String!
  status: PostStatus!
}
```

### **2.6 Интерфейсы**

```graphql
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
}

type Post implements Node {
  id: ID!
  title: String!
}
```

### **2.7 Union типы**

```graphql
union SearchResult = User | Post | Comment

type Query {
  search(query: String!): [SearchResult!]!
}
```

---

## **3. Операции GraphQL**

### **3.1 Query (Запросы)**

```graphql
# Простой запрос
query {
  user(id: "1") {
    name
    email
  }
}

# Запрос с переменными
query GetUser($userId: ID!) {
  user(id: $userId) {
    name
    email
    posts {
      title
      createdAt
    }
  }
}

# Множественные запросы
query {
  currentUser: user(id: "1") {
    name
  }
  allPosts: posts {
    title
  }
}
```

### **3.2 Mutation (Изменения)**

```graphql
# Создание пользователя
mutation {
  createUser(input: {
    name: "John Doe"
    email: "john@example.com"
  }) {
    id
    name
    createdAt
  }
}

# Обновление поста
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
  updatePost(id: $id, input: $input) {
    id
    title
    updatedAt
  }
}
```

### **3.3 Subscription (Подписки)**

```graphql
# Подписка на новые посты
subscription {
  postAdded {
    id
    title
    author {
      name
    }
  }
}

# Подписка с фильтрацией
subscription PostsByAuthor($authorId: ID!) {
  postAdded(authorId: $authorId) {
    id
    title
    content
  }
}
```

---

## **4. Директивы**

### **4.1 Встроенные директивы**

#### **@include и @skip**

```graphql
query GetUser($includeEmail: Boolean!, $skipPosts: Boolean!) {
  user(id: "1") {
    name
    email @include(if: $includeEmail)
    posts @skip(if: $skipPosts) {
      title
    }
  }
}
```

#### **@deprecated**

```graphql
type User {
  id: ID!
  name: String!
  username: String @deprecated(reason: "Use 'name' instead")
}
```

### **4.2 Пользовательские директивы**

```graphql
directive @auth(role: String!) on FIELD_DEFINITION
directive @rateLimit(max: Int!, window: Int!) on FIELD_DEFINITION

type Query {
  adminUsers: [User!]! @auth(role: "ADMIN")
  searchUsers: [User!]! @rateLimit(max: 100, window: 60)
}
```

---

## **5. Продвинутые концепции**

### **5.1 Фрагменты**

```graphql
# Определение фрагмента
fragment UserInfo on User {
  id
  name
  email
}

# Использование фрагмента
query {
  user(id: "1") {
    ...UserInfo
    posts {
      title
    }
  }
}

# Inline фрагменты
query {
  search(query: "GraphQL") {
    ... on User {
      name
      email
    }
    ... on Post {
      title
      content
    }
  }
}
```

### **5.2 Пагинация**

#### **Offset-based**

```graphql
type Query {
  posts(offset: Int, limit: Int): [Post!]!
}

query {
  posts(offset: 0, limit: 10) {
    id
    title
  }
}
```

#### **Cursor-based (Relay)**

```graphql
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type Query {
  posts(first: Int, after: String): PostConnection!
}
```

### **5.3 DataLoader (решение N+1 проблемы)**

```python
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        # Загружаем всех пользователей одним запросом
        users = await db.users.find({"id": {"$in": user_ids}})
        # Возвращаем в том же порядке, что и user_ids
        return [users_dict.get(user_id) for user_id in user_ids]

# Использование в резолвере
async def resolve_author(post, info):
    user_loader = info.context["user_loader"]
    return await user_loader.load(post.author_id)
```

---

## **6. Сравнение подходов**

### **6.1 GraphQL vs REST**

| **Критерий**                | **REST**                                      | **GraphQL**                   |
| ----------------------------------------- | --------------------------------------------------- | ----------------------------------- |
| **Эндпоинты**              | Множественные (`/users`, `/posts`) | Один (`/graphql`)             |
| **Структура ответа** | Фиксированная                          | Гибкая                        |
| **Over-fetching**                   | Часто                                          | Нет                              |
| **Under-fetching**                  | Часто (N+1 запросов)                   | Нет                              |
| **Кэширование**          | HTTP-кэш (простое)                        | Сложное                      |
| **Файлы**                      | Нативная поддержка                 | Требует расширений |
| **Кривая обучения**   | Низкая                                        | Высокая                      |
| **Инструменты**          | Зрелые                                        | Развивающиеся          |

### **6.2 GraphQL vs gRPC**

| **Критерий**                     | **GraphQL**                   | **gRPC**              |
| ---------------------------------------------- | ----------------------------------- | --------------------------- |
| **Протокол**                     | HTTP/1.1, HTTP/2                    | HTTP/2                      |
| **Формат**                         | JSON                                | Protocol Buffers            |
| **Типизация**                   | Schema (SDL)                        | .proto файлы           |
| **Streaming**                            | Subscriptions                       | Bidirectional               |
| **Браузеры**                     | Нативная поддержка | Требует прокси |
| **Производительность** | Средняя                      | Высокая              |

### **6.3 Когда использовать GraphQL**

**✅ Используйте GraphQL когда:**

- Множество клиентов с разными потребностями
- Сложные связи между данными
- Мобильные приложения (важен размер ответа)
- Быстрая разработка фронтенда
- Нужна интроспекция API

**❌ Не используйте GraphQL когда:**

- Простое CRUD API
- Файловые операции
- Критична производительность
- Команда не готова к сложности
- Нужно простое кэширование

---

## **7. Безопасность в GraphQL**

### **7.1 Основные угрозы**

#### **Query Depth Attack**

```graphql
# Злонамеренный запрос
query {
  user {
    posts {
      author {
        posts {
          author {
            posts {
              # ... бесконечная вложенность
            }
          }
        }
      }
    }
  }
}
```

#### **Query Complexity Attack**

```graphql
# Дорогой запрос
query {
  posts {
    comments {
      author {
        posts {
          comments {
            # ... множество связей
          }
        }
      }
    }
  }
}
```

### **7.2 Защитные механизмы**

#### **Ограничение глубины**

```python
from graphql import validate, DepthLimitValidationRule

# Максимальная глубина запроса
validation_rules = [DepthLimitValidationRule(max_depth=10)]
schema = strawberry.Schema(query=Query, validation_rules=validation_rules)
```

#### **Анализ сложности**

```python
from strawberry.extensions import QueryComplexityLimiter

schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryComplexityLimiter(maximum_query_complexity=1000)
    ]
)
```

#### **Rate Limiting**

```python
from strawberry.extensions import AddValidationRules
from graphql_query_complexity import ComplexityLimitValidationRule

# Ограничение по времени
@strawberry.field
def expensive_field(self, info) -> str:
    # Проверяем rate limit для пользователя
    user_id = info.context["user_id"]
    if not rate_limiter.allow(user_id):
        raise Exception("Rate limit exceeded")
    return "result"
```

### **7.3 Аутентификация и авторизация**

```python
import strawberry
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"
  
    def has_permission(self, source, info, **kwargs):
        return info.context.get("user") is not None

class IsOwner(BasePermission):
    message = "User is not the owner"
  
    def has_permission(self, source, info, **kwargs):
        user = info.context.get("user")
        return user and source.author_id == user.id

@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def create_post(self, title: str, content: str) -> Post:
        # Только аутентифицированные пользователи
        pass
  
    @strawberry.mutation(permission_classes=[IsOwner])
    def delete_post(self, post_id: int) -> bool:
        # Только владелец поста
        pass
```

---

## **8. Инструменты и экосистема**

### **8.1 Серверные библиотеки Python**

| **Библиотека** | **Особенности**   | **Использование** |
| ------------------------------ | ---------------------------------- | ------------------------------------ |
| **Strawberry**           | Современная, type hints | Новые проекты            |
| **Graphene**             | Зрелая, популярная | Enterprise                           |
| **Ariadne**              | Schema-first подход          | Большие команды        |
| **Tartiflette**          | Асинхронная             | Высокая нагрузка      |

### **8.2 Клиентские библиотеки**

- **Apollo Client** (React, Vue, Angular)
- **Relay** (React, сложные приложения)
- **urql** (React, легковесная)
- **graphql-request** (простые запросы)

### **8.3 Инструменты разработки**

- **GraphQL Playground** – интерактивная IDE
- **GraphiQL** – браузерная IDE
- **Apollo Studio** – мониторинг и аналитика
- **GraphQL Code Generator** – генерация типов

---

---

## **2. Практика: Создаем GraphQL-API**

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
