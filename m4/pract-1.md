### Проектирование API на JSON-RPC:   

Рассмотрим пример **JSON-RPC сервера** на Python, который реализует:  
- Метод для сложения чисел (`add`).  
- Метод для получения информации о пользователе (`get_user`).  

Используем библиотеку `jsonrpcserver` (для сервера) и `jsonrpcclient` (для клиента).  

---

## 1. Установка библиотек 
```bash
pip install jsonrpcserver jsonrpcclient aiohttp  
```
*(`aiohttp` нужен для асинхронного HTTP-сервера.)*  

---

## **2. Сервер (API)**  
Файл `server.py`:  
```python
from aiohttp import web
from jsonrpcserver import method, async_dispatch, Success

# Регистрируем методы API
@method
async def add(a, b):
    return Success(a + b)

@method
async def get_user(user_id):
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    return Success({"id": user_id, "name": users.get(user_id, "Unknown")})

# Обработчик JSON-RPC запросов
async def handle_rpc(request):
    request_data = await request.text()
    response = await async_dispatch(request_data)
    return web.json_response(response)

app = web.Application()
app.router.add_post("/rpc", handle_rpc)

if __name__ == "__main__":
    web.run_app(app, port=5000)
```

#### **Как это работает?**  
1. Сервер запускается на `http://localhost:5000/rpc`.  
2. Принимает POST-запросы в формате JSON-RPC.  
3. Поддерживает два метода:  
   - `add(a, b)` → возвращает сумму.  
   - `get_user(user_id)` → возвращает имя пользователя.  

---

## **3. Клиент**  
Файл `client.py`:  
```python
import asyncio
from jsonrpcclient import Ok, parse_json, request_json

async def main():
    # Пример запроса к методу `add`
    add_request = request_json("add", params=[2, 3])
    print("Запрос (add):", add_request)

    # Пример запроса к методу `get_user`
    user_request = request_json("get_user", params=[2])
    print("Запрос (get_user):", user_request)

    # Отправляем запросы на сервер (можно через `aiohttp`, `requests` и т.д.)
    # Здесь просто парсим ответ вручную для демонстрации
    add_response = parse_json('{"jsonrpc": "2.0", "result": 5, "id": 1}')
    if isinstance(add_response, Ok):
        print("Результат (add):", add_response.result)  # 5

    user_response = parse_json('{"jsonrpc": "2.0", "result": {"id": 2, "name": "Bob"}, "id": 2}')
    if isinstance(user_response, Ok):
        print("Результат (get_user):", user_response.result)  # {'id': 2, 'name': 'Bob'}

asyncio.run(main())
```

#### **Вывод клиента:**  
```
Запрос (add): {"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}
Запрос (get_user): {"jsonrpc": "2.0", "method": "get_user", "params": [2], "id": 2}
Результат (add): 5
Результат (get_user): {'id': 2, 'name': 'Bob'}
```

---

## **4. Тестирование через HTTP (curl)**  
Отправка запроса к серверу:  
```bash
curl -X POST http://localhost:5000/rpc -d '{"jsonrpc": "2.0", "method": "add", "params": [5, 7], "id": 1}' -H "Content-Type: application/json"
```

**URL-формат запроса (GET):**
```
http://localhost:5000/rpc?jsonrpc=2.0&method=add&params[]=5&params[]=7&id=1
```

**Примечание:** Для работы с GET-запросами необходимо модифицировать сервер, чтобы он обрабатывал не только POST, но и GET запросы. В исходной версии сервера поддерживаются только POST-запросы, поэтому при попытке открыть URL в браузере вы получите ошибку `405: Method Not Allowed`.



**Ответ:**  
```json
{"jsonrpc": "2.0", "result": 12, "id": 1}
```

---

## **5. Улучшенный сервер с поддержкой GET-запросов**

Файл `server_with_get.py`:
```python
from aiohttp import web
import json
from jsonrpcserver import method, async_dispatch, Success

# Регистрируем методы API
@method
async def add(a, b):
    return Success(a + b)

@method
async def get_user(user_id):
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    return Success({"id": user_id, "name": users.get(user_id, "Unknown")})

# Обработчик POST JSON-RPC запросов
async def handle_post_rpc(request):
    request_data = await request.text()
    response = await async_dispatch(request_data)
    return web.json_response(response)

# Обработчик GET JSON-RPC запросов
async def handle_get_rpc(request):
    # Получаем параметры из URL
    params = request.query
    
    # Формируем JSON-RPC запрос из параметров URL
    jsonrpc_request = {
        "jsonrpc": params.get("jsonrpc", "2.0"),
        "method": params.get("method"),
        "id": params.get("id", "1")
    }
    
    # Обрабатываем параметры
    if "params[]" in params:
        # Если параметры переданы как params[]=value1&params[]=value2
        jsonrpc_request["params"] = [
            int(p) if p.isdigit() else p 
            for p in request.query.getall("params[]")
        ]
    elif "params" in params:
        # Если параметры переданы как строка JSON
        try:
            jsonrpc_request["params"] = json.loads(params["params"])
        except:
            jsonrpc_request["params"] = params["params"]
    
    # Выполняем запрос
    response = await async_dispatch(json.dumps(jsonrpc_request))
    return web.json_response(response)

app = web.Application()
# Регистрируем обработчики для POST и GET запросов
app.router.add_post("/rpc", handle_post_rpc)
app.router.add_get("/rpc", handle_get_rpc)

if __name__ == "__main__":
    web.run_app(app, port=5000)
```

## **6. Итог**  
✅ **Сервер:**  
- Принимает JSON-RPC запросы.  
- Реализует методы `add` и `get_user`.  

✅ **Клиент:**  
- Формирует JSON-RPC запросы.  
- Обрабатывает ответы.  

✅ **Преимущества подхода:**  
- **Простота** – не нужно продумывать REST-эндпоинты.  
- **Гибкость** – можно добавлять любые методы.  
- **Легковесность** – минимум кода.  

🚀 **Доработки (если нужно):**  
- Добавить аутентификацию.  
- Подключить базу данных (например, SQLite).  
- Реализовать пакетные запросы (`batch`).  

Готово! Теперь у вас есть рабочий пример JSON-RPC API на Python. 😊