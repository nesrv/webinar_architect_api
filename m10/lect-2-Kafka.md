### **Урок: Интеграции для профессионалов**  
**Связь с предыдущим уроком:**  
Развитие event-based API из прошлого урока – добавляем продвинутые техники интеграции и масштабирования.  
**Длительность:** 1 час  
**Уровень:** Продвинутый  
**Формат:** Практика + Разбор кейсов  

---

## **1. Переход от простого чата к enterprise-решению **  
### **1.1 Проблемы предыдущей реализации**  
- Нет истории сообщений  
- Нет отказоустойчивости  
- Нет балансировки нагрузки  

### **1.2 Архитектура профессионального решения**  
```mermaid
graph TD
    A[Клиент] -->|WebSocket| B[API Gateway]
    B --> C[Сервис аутентификации]
    B --> D[Сервис чата]
    D --> E[Redis Streams]
    E --> F[История в PostgreSQL]
    E --> G[Аналитика в Kafka]
```

---

## **2. Практика: Модернизация системы **  
### **2.1 Установка**  
```bash
pip install fastapi uvicorn websockets redis kafka-python sqlalchemy
```

### **2.2 Код сервиса чата с историей**  
Файл `chat_service.py`:  
```python
from fastapi import FastAPI, WebSocket
import redis
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Настройка Redis и PostgreSQL
r = redis.Redis(host='redis', port=6379)
engine = create_engine('postgresql://user:pass@postgres:5432/chat')
Base = declarative_base()

# Модель для хранения истории
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = FastAPI()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    pubsub = r.pubsub()
    pubsub.subscribe("chat_channel")
    
    async def save_to_db(message):
        session = Session()
        session.add(Message(user_id=message['user_id'], text=message['text']))
        session.commit()
        session.close()

    try:
        while True:
            data = await websocket.receive_text()
            message = {"user_id": user_id, "text": data}
            
            # Сохраняем в Redis и PostgreSQL
            r.publish("chat_channel", json.dumps(message))
            await save_to_db(message)
            
    except Exception as e:
        print(f"Ошибка: {e}")
```

### **2.3 Интеграция с Kafka для аналитики**  
Файл `analytics_consumer.py`:  
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'chat_analytics',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    msg = message.value
    print(f"Аналитика: {msg['user_id']} отправил сообщение в {msg['timestamp']}")
```

---

## **3. Разбор профессиональных кейсов **  
### **3.1 Паттерны интеграции**  
- **Dead Letter Queue:** Обработка неудачных сообщений  
- **Circuit Breaker:** Защита от каскадных ошибок  
- **Outbox Pattern:** Гарантированная доставка  

### **3.2 Мониторинг**  
```bash
# Prometheus + Grafana
docker run -p 9090:9090 prom/prometheus
docker run -p 3000:3000 grafana/grafana
```

---

## **4. Домашнее задание**  
1. Реализуйте DLQ для Redis  
2. Добавьте Circuit Breaker в WebSocket-обработчик  
3. Настройте Grafana для мониторинга активности чата  

---

## **5. Полезные ресурсы**  
- [Redis Streams](https://redis.io/topics/streams-intro)  
- [Kafka Python](https://kafka-python.readthedocs.io/)  
- [Microservices Patterns](https://microservices.io/patterns/)  

🚀 **Результат:** Промышленное event-based решение с гарантией доставки и аналитикой!