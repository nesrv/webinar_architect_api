# Проектирование архитектуры и интеграций сервисов


* Модуль 1. Введение.
* Модуль 2. Как работает интернет.
* Модуль 3. Введение про АРІ.
* Модуль 4. Проектирование API - JSON-RPC.
* Модуль 5. Проектирование AP – SOAP.
* Модуль 6. Проектирование API – GraphQL.
* Модуль 7. Проектирование API – gRPC.
* Модуль 8. Проектирование AP - REST.
* Модуль 9. Event-based (событийно-ориентированные) асинхронные АРІ.
* Модуль 10. Интеграции для профессионалов.
* Модуль 11. Брокеры сообщений.
* Модуль 12. Solution Architecture и System Design - Введение.
* Модуль 13. Solution Architecture и System Design - Технологические подходы.
* Модуль 14. Проектирование баз данных SQL.
* Модуль 15. Проектирование баз данных NoSQL и DWH.


Для проведения курса по проектированию API и системной архитектуре на **Python** вам понадобится следующий программный стенд:  



### **1. Основные инструменты разработки**  
- ** Python 3.10+** (последняя стабильная версия)  
- ** VS Code** / Cursor (с расширениями: Python, Docker, REST Client)  
- **Jupyter Notebook / JupyterLab** (для интерактивных примеров в модулях по БД и анализу)  
- **Docker + Docker Compose** (развертывание брокеров сообщений, БД и микросервисов)  

### **2. Библиотеки Python** (установка через `pip`)  
#### **API и протоколы**  
- **REST**: `FastAPI`  + `uvicorn` (ASGI-сервер)  
- **GraphQL**: `graphene` или `strawberry`  
- **gRPC**: `grpcio`, `grpcio-tools`, `protobuf`  
- **SOAP**: `zeep` (клиент), `spyne` (сервер)  
- **JSON-RPC**: `json-rpc` (или `FastAPI` с ручной реализацией)  
- **Event-based API**: `FastAPI + WebSockets`, `aio-pika` (RabbitMQ), `confluent-kafka`  

#### **Базы данных**  
- **SQL**: `SQLAlchemy` (ORM), `psycopg2` (PostgreSQL), `aiomysql` (асинхронный MySQL)  
- **NoSQL**: `pymongo` (MongoDB), `redis` (Redis)  
- **DWH**: `pandas`, `sqlalchemy` (для анализа), `pyarrow` (Apache Parquet)  

#### **Тестирование и документация**  
- `pytest` (юнит-тесты)  
- `Postman`  
- `Swagger UI` (встроен в FastAPI)  


### **3. Внешние сервисы и инфраструктура**  
- **Брокеры сообщений** (развертываются в Docker):    
  - **RabbitMQ**: `rabbitmq:3-management` (с веб-интерфейсом)  
- **Базы данных** (можно в Docker или облачные):  
  - **PostgreSQL**: `postgres:latest`  
  - **MongoDB**: `mongo:latest`  
  - **Redis**: `redis:alpine`  

### **4. Вспомогательные инструменты**  
- **Git** (версионный контроль) + **GitHub**  
- **NGINX** (обратный прокси для API, опционально)  
- **Prometheus + Grafana** (мониторинг, для модуля по System Design)  


### **5. Готовые Docker-образы для быстрого старта**  
Пример `docker-compose.yml` для развертывания инфраструктуры:  
```yaml
version: '3'
services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_PASSWORD: "password"
    ports:
      - "5432:5432"

  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"  # Web UI

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    ports:
      - "2181:2181"
```

### **6. Альтернативные облачные решения**  
Если локальные ресурсы ограничены, можно использовать:  
- **MongoDB Atlas** (бесплатный кластер)  
- **CloudAMQP** (RabbitMQ в облаке)  
- **Confluent Cloud** (Kafka as a Service)  

### **Итог**  
Минимальный набор: **Python + FastAPI + Docker (PostgreSQL, MongoDB, RabbitMQ/Kafka)**.  
Для углубленного изучения: добавить **Prometheus/Grafana** и **Terraform**.  

Если нужны готовые примеры кода или шаблоны проектов – уточните модули, и я предоставлю конкретные репозитории.