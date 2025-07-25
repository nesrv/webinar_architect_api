# Blog REST API

REST API для управления постами и комментариями блога на FastAPI.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn main:app --reload
```

## Документация

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Примеры запросов

### Получить все посты
```bash
curl http://localhost:8000/posts
```

### Создать пост
```bash
curl -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -d '{"id": 2, "title": "Новый пост", "content": "Еще текст"}'
```

### Получить комментарии к посту
```bash
curl http://localhost:8000/posts/1/comments
```

### Удалить пост
```bash
curl -X DELETE http://localhost:8000/posts/1
```