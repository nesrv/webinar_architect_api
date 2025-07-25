from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Blog API",
    description="REST API для управления постами и комментариями",
    version="1.0.0"
)

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

# Получить все посты
@app.get("/posts", 
         response_model=List[Post],
         summary="Получить все посты",
         description="Возвращает список всех постов в блоге")
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