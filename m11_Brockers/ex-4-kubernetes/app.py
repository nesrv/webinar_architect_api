from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI()

messages = []

class Message(BaseModel):
    user: str
    text: str

@app.get("/")
def index():
    return FileResponse('index.html')

@app.get("/messages")
def get_messages():
    return messages

@app.post("/messages")
def add_message(message: Message):
    messages.append(message.dict())
    return {"ok": True}

@app.get("/health")
def health():
    return {"status": "ok", "pod": os.environ.get("HOSTNAME", "unknown")}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)