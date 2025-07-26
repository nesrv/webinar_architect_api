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