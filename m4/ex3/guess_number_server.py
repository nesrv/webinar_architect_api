from aiohttp import web
from jsonrpcserver import method, async_dispatch, Success
import random
import asyncio

# Хранилище игровых сессий
games = {}

@method
async def start_game(difficulty="normal"):
    """Начать новую игру
    difficulty: easy (1-50), normal (1-100), hard (1-200)
    """
    # Определяем диапазон чисел в зависимости от сложности
    ranges = {
        "easy": 50,
        "normal": 100,
        "hard": 200
    }
    max_number = ranges.get(difficulty, 100)
    
    # Генерируем случайное число и создаем ID игры
    game_id = f"game_{len(games) + 1}"
    secret_number = random.randint(1, max_number)
    attempts = 0
    
    # Сохраняем игру
    games[game_id] = {
        "secret_number": secret_number,
        "attempts": attempts,
        "max_number": max_number,
        "status": "active",
        "history": []
    }
    
    return Success({
        "game_id": game_id,
        "message": f"Новая игра создана! Угадайте число от 1 до {max_number}.",
        "difficulty": difficulty
    })

@method
async def guess(game_id, number):
    """Сделать попытку угадать число"""
    # Проверяем существование игры
    if game_id not in games:
        return Success({"error": "Игра не найдена"})
    
    game = games[game_id]
    
    # Проверяем, не закончена ли игра
    if game["status"] != "active":
        return Success({
            "error": "Игра уже завершена",
            "message": f"Загаданное число было {game['secret_number']}"
        })
    
    # Увеличиваем счетчик попыток
    game["attempts"] += 1
    
    # Проверяем число
    secret = game["secret_number"]
    guess_number = int(number)
    
    # Добавляем в историю
    game["history"].append(guess_number)
    
    # Определяем результат
    if guess_number < secret:
        result = {
            "message": "Загаданное число больше",
            "attempts": game["attempts"]
        }
    elif guess_number > secret:
        result = {
            "message": "Загаданное число меньше",
            "attempts": game["attempts"]
        }
    else:
        game["status"] = "won"
        result = {
            "message": f"Поздравляем! Вы угадали число {secret}!",
            "attempts": game["attempts"],
            "status": "won"
        }
    
    return Success(result)

@method
async def get_hint(game_id):
    """Получить подсказку"""
    if game_id not in games:
        return Success({"error": "Игра не найдена"})
    
    game = games[game_id]
    
    if game["status"] != "active":
        return Success({
            "error": "Игра уже завершена",
            "message": f"Загаданное число было {game['secret_number']}"
        })
    
    secret = game["secret_number"]
    
    # Генерируем подсказку
    if secret % 2 == 0:
        hint = "Число четное"
    else:
        hint = "Число нечетное"
        
    # Дополнительные подсказки
    if game["attempts"] >= 3:
        if secret % 5 == 0:
            hint += " и делится на 5"
        else:
            hint += " и не делится на 5"
    
    if game["attempts"] >= 5:
        if secret <= game["max_number"] // 2:
            hint += f" и находится в первой половине диапазона (1-{game['max_number']//2})"
        else:
            hint += f" и находится во второй половине диапазона ({game['max_number']//2+1}-{game['max_number']})"
    
    return Success({
        "hint": hint,
        "attempts": game["attempts"]
    })

@method
async def give_up(game_id):
    """Сдаться и узнать загаданное число"""
    if game_id not in games:
        return Success({"error": "Игра не найдена"})
    
    game = games[game_id]
    
    if game["status"] != "active":
        return Success({
            "error": "Игра уже завершена",
            "message": f"Загаданное число было {game['secret_number']}"
        })
    
    game["status"] = "lost"
    
    return Success({
        "message": f"Вы сдались. Загаданное число было {game['secret_number']}.",
        "attempts": game["attempts"],
        "status": "lost"
    })

@method
async def game_stats(game_id):
    """Получить статистику игры"""
    if game_id not in games:
        return Success({"error": "Игра не найдена"})
    
    game = games[game_id]
    
    return Success({
        "attempts": game["attempts"],
        "status": game["status"],
        "history": game["history"],
        "max_number": game["max_number"],
        "secret_number": game["secret_number"] if game["status"] != "active" else "???"
    })

# Обработчик JSON-RPC запросов
async def handle_rpc(request):
    request_data = await request.text()
    response = await async_dispatch(request_data)
    return web.json_response(response)

# Запуск сервера
async def start_server():
    app = web.Application()
    app.router.add_post("/api", handle_rpc)
    app.router.add_get("/api", handle_rpc)  # Для удобства тестирования
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 5000)
    await site.start()
    print("Игровой сервер запущен на http://localhost:5000/api")
    
    # Держим сервер запущенным
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_server())