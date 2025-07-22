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
