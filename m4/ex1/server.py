from aiohttp import web
from jsonrpcserver import method, async_dispatch

# Регистрируем методы API
@method
async def add(a, b):
    return {"result": a + b}

@method
async def get_user(user_id):
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    return {"id": user_id, "name": users.get(user_id, "Unknown")}

# Обработчик JSON-RPC запросов
async def handle_rpc(request):
    request_data = await request.text()
    response = await async_dispatch(request_data)
    return web.json_response(response)

app = web.Application()
app.router.add_post("/rpc", handle_rpc)

if __name__ == "__main__":
    web.run_app(app, port=5000)