### **Практическое занятие: SOAP API на FastAPI**

---

## **1. Введение**

### **1.1 Можно ли использовать FastAPI для SOAP?**

FastAPI не поддерживает SOAP "из коробки", но можно:

1. **Интегрировать библиотеку `spyne`** (как в примере выше).
2. **Использовать `zeep` для клиента** + FastAPI как прокси.
3. **Переделать API в REST/JSON-RPC** (если SOAP не обязателен).

В этом примере создадим **гибридный сервис**: FastAPI будет принимать HTTP-запросы и делегировать их SOAP-серверу.

---

## **2. Практическая часть**

### **Задание: FastAPI + SOAP (spyne) для управления пользователями**

**Цель:**

- FastAPI принимает REST-запросы.
- Внутри вызывает SOAP-сервис (`get_user`, `create_user`).

#### **Шаг 1: Установка библиотек**

```bash
pip install fastapi spyne uvicorn zeep
```

#### **Шаг 2: Создание SOAP-сервиса (spyne)**

Файл `soap_service.py`:

```python
from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class UserService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def get_user(ctx, user_id):
        users = {1: "Alice", 2: "Bob"}
        return users.get(user_id, "User not found")

    @rpc(Unicode, _returns=Unicode)
    def create_user(ctx, name):
        return f"User {name} created"

application = Application(
    [UserService],
    tns="http://example.com/user-service",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

soap_app = WsgiApplication(application)
```

#### **Шаг 3: FastAPI как обертка для SOAP**

Файл `main.py`:

```python
from fastapi import FastAPI, HTTPException
from zeep import Client

app = FastAPI()
SOAP_URL = "http://localhost:8000/soap"  # Эндпоинт SOAP-сервиса

# Клиент для SOAP (zeep)
soap_client = Client(f"{SOAP_URL}?wsdl")

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    try:
        result = soap_client.service.get_user(user_id)
        return {"user": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/user")
async def create_user(name: str):
    try:
        result = soap_client.service.create_user(name)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

#### **Шаг 4: Запуск**

1. **Запустите SOAP-сервис** (отдельно в терминале):

   ```bash
   gunicorn soap_service:soap_app -b 0.0.0.0:8000
   ```

   - Проверьте WSDL: http://localhost:8000/?wsdl
2. **Запустите FastAPI**:

   ```bash
   uvicorn main:app --reload
   ```

   - API будет доступно на http://localhost:8000/docs

---

## **3. Тестирование (10 минут)**

### **Через FastAPI (REST-интерфейс)**

1. **GET /user/1** → Вернет `{"user": "Alice"}`.
2. **POST /user** с телом `{"name": "Charlie"}` → Вернет `{"message": "User Charlie created"}`.

### **Прямой SOAP-запрос (curl)**

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: text/xml" \
  -d '
  <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:usr="http://example.com/user-service">
    <soapenv:Body>
      <usr:get_user>
        <usr:user_id>2</usr:user_id>
      </usr:get_user>
    </soapenv:Body>
  </soapenv:Envelope>'
```

---

## **4. Плюсы и минусы подхода**

### **✅ Плюсы:**

- **Документация Swagger** для REST-части.
- **Легаси-интеграция** – если старый SOAP-сервис нельзя заменить.

### **❌ Минусы:**

- **Двойная конвертация** (REST → SOAP → REST).
- **Производительность** – дополнительные накладные расходы.

---

## **5. Альтернативы**

1. **Полный переход на REST** (если SOAP не обязателен).
2. **Использование gRPC** вместо SOAP для внутренних сервисов.

---

## **6. Итоги**

- **FastAPI + SOAP** – рабочий вариант для интеграции с легаси-системами.
- **Лучше использовать REST/GraphQL**, если нет жестких требований к SOAP.

**Дальнейшие шаги:**

1. Добавьте валидацию данных через Pydantic.
2. Реализуйте аутентификацию (JWT для FastAPI + WS-Security для SOAP).
