Реализация JSON-RPC сервер с поддержкой методов, эквивалентных `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, используя **`aiohttp`**:

В отличие от REST API, который использует HTTP-методы (GET, POST, PUT, PATCH, DELETE) как семантические действия, JSON-RPC всегда использует только HTTP POST (в большинстве реализаций) и описывает действие в теле запроса через поле "method".

### ✅ Пример JSON-RPC сервера на `aiohttp`

```python
from aiohttp import web
import json

routes = web.RouteTableDef()

# Пример: функции-обработчики JSON-RPC методов
async def get_user(params):
    user_id = params.get("id")
    # Тут обычно запрос в БД
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}

async def create_user(params):
    # Добавить в БД
    return {"id": 123, **params}

async def update_user(params):
    return {"status": "updated", "data": params}

async def patch_user(params):
    return {"status": "patched", "data": params}

async def delete_user(params):
    return {"status": "deleted", "id": params.get("id")}

# Маршрут JSON-RPC
@routes.post("/api/jsonrpc")
async def jsonrpc_handler(request):
    try:
        data = await request.json()
        method = data.get("method")
        params = data.get("params", {})
        rpc_id = data.get("id")

        methods = {
            "getUser": get_user,
            "createUser": create_user,
            "updateUser": update_user,
            "patchUser": patch_user,
            "deleteUser": delete_user,
        }

        if method not in methods:
            raise Exception(f"Method '{method}' not found")

        result = await methods[method](params)

        return web.json_response({
            "jsonrpc": "2.0",
            "result": result,
            "id": rpc_id
        })

    except Exception as e:
        return web.json_response({
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": str(e)},
            "id": data.get("id")
        }, status=500)

# Примеры функций
def create_user(params):
    # Вставить в БД, например
    return {"id": 123, **params}

# Остальные функции - аналогично

# Запуск приложения
app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8080)
```

---

### 🔧 Пример запроса:

```json
POST /api/jsonrpc
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "createUser",
  "params": {
    "name": "Bob",
    "email": "bob@example.com"
  },
  "id": 1
}
```

### 📤 Ответ:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "id": 123,
    "name": "Bob",
    "email": "bob@example.com"
  },
  "id": 1
}
```


