### **Урок: Интеграции для профессионалов**  
**Связь с предыдущим уроком:**  
Развитие event-based API из прошлого урока – добавляем продвинутые техники интеграции и масштабирования.  


---

Apache Kafka — это **распределённая потоковая платформа**, предназначенная для обработки событий в реальном времени, передачи сообщений между системами и хранения потоковых данных. Вот как она работает:

---

## 🔹 **Основные концепции Kafka**
### 1. **Топики (Topics)**
   - Это "категории" или "логические каналы", в которые записываются сообщения.
   - Пример: `user_actions`, `payment_transactions`, `sensor_data`.
   - Сообщения в топиках **упорядочены** и **неизменяемы** (после записи их нельзя изменить).

### 2. **Партиции (Partitions)**
   - Каждый топик делится на партиции для **масштабируемости**.
   - Сообщения в одной партиции упорядочены по времени (каждое имеет **offset** — уникальный номер).
   - Данные реплицируются между серверами для отказоустойчивости.

### 3. **Производители (Producers)**
   - Приложения, которые **публикуют** сообщения в топики.
   - Могут указывать партицию для записи (или использовать балансировку).

### 4. **Потребители (Consumers)**
   - Приложения, которые **читают** сообщения из топиков.
   - Работают в **группах потребителей (Consumer Groups)** для распределённой обработки.

### 5. **Брокеры (Brokers)**
   - Серверы Kafka, хранящие данные топиков.
   - Объединяются в **кластер** для отказоустойчивости.

### 6. **ZooKeeper (в старых версиях)**
   - Управлял метаданными кластера (в Kafka 3.0+ заменён на **Kafka Raft**).

---

## 🔹 **Как данные перемещаются в Kafka?**
1. **Producer** отправляет сообщение в топик (например, `logs`):
   ```python
   producer.send("logs", key="server1", value="Error: Disk full")
   ```
2. **Брокер** принимает сообщение и записывает его в партицию топика.
3. **Consumer** читает сообщения из партиций:
   ```python
   for message in consumer:
       print(message.value)  # "Error: Disk full"
   ```
4. Данные **хранятся** на диске (можно настраивать срок хранения).

---

## 🔹 **Ключевые особенности Kafka**
### ✅ Высокая пропускная способность
   - Обрабатывает **миллионы сообщений в секунду**.
   - Данные записываются на диск **последовательно**, что ускоряет работу.

### ✅ Отказоустойчивость
   - Данные реплицируются между брокерами (по умолчанию — 3 копии).
   - При падении брокера потребители автоматически переключаются на реплику.

### ✅ Горизонтальное масштабирование
   - Можно добавлять брокеры и партиции для увеличения нагрузки.

### ✅ Поддержка потоковой обработки
   - Интеграция с **Kafka Streams**, **Spark**, **Flink** для аналитики в реальном времени.

---

## 🔹 **Пример архитектуры с Kafka**
```
Продюсеры (веб-приложение, IoT) → Kafka (топики) → Потребители (аналитика, БД, нотификации)
```

---

## 🔹 **Когда использовать Kafka?**
1. **Микросервисы**: Асинхронный обмен сообщениями между сервисами.
2. **Логирование**: Централизованный сбор логов с тысяч серверов.
3. **Транзакции**: Обработка платежей в реальном времени.
4. **Аналитика**: Потоковая обработка данных (например, кликов в рекламе).
5. **Event Sourcing**: Хранение истории всех событий в системе.

---

## 🔹 **Пример кода на Python**
### Producer:
```python
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})
producer.produce("orders", key="user123", value="New order: iPhone")
producer.flush()
```

### Consumer:
```python
from confluent_kafka import Consumer

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "order-processors",
    "auto.offset.reset": "earliest"
})
consumer.subscribe(["orders"])

while True:
    msg = consumer.poll(1.0)
    if msg: 
        print(f"Обработан заказ: {msg.value()}")
```

---

## 🔹 **Чем Kafka отличается от RabbitMQ?**
| Характеристика      | Kafka                          | RabbitMQ                     |
|---------------------|--------------------------------|------------------------------|
| **Модель**          | Публикация/подписка           | Очереди (Point-to-Point)     |
| **Скорость**        | Очень высокая (дисковая запись)| Высокая (RAM)               |
| **Хранение**        | Сохраняет сообщения долго     | Удаляет после обработки     |
| **Использование**   | Потоковая обработка           | Фоновые задачи (Celery)     |

---

## **Вывод**
Kafka — это **не просто очередь**, а **распределённый журнал событий** для:
- Обработки потоковых данных,
- Построения Event-Driven архитектур,
- Создания надежных pipelines между системами.

Для старта можно развернуть локальный кластер через `docker-compose` или использовать облачные решения (Confluent Cloud, AWS MSK).


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