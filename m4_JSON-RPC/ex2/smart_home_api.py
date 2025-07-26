from aiohttp import web
from jsonrpcserver import method, async_dispatch, Success
import asyncio
import random

# Имитация состояния устройств умного дома
smart_home = {
    "devices": {
        "light_living_room": {"status": "off", "brightness": 0, "type": "light"},
        "light_kitchen": {"status": "off", "brightness": 0, "type": "light"},
        "thermostat": {"status": "on", "temperature": 22, "type": "climate"},
        "tv": {"status": "off", "channel": 1, "volume": 20, "type": "media"},
        "door_lock": {"status": "locked", "type": "security"}
    },
    "scenes": {
        "movie_night": ["light_living_room", "tv"],
        "cooking": ["light_kitchen", "thermostat"],
        "away": ["light_living_room", "light_kitchen", "thermostat", "tv", "door_lock"]
    }
}

# Имитация датчиков
async def update_sensors():
    while True:
        smart_home["sensors"] = {
            "temperature": round(random.uniform(18, 25), 1),
            "humidity": round(random.uniform(40, 60), 1),
            "motion_detected": random.choice([True, False])
        }
        await asyncio.sleep(5)

# API методы
@method
async def get_device_status(device_id):
    """Получить статус устройства"""
    if device_id in smart_home["devices"]:
        return Success(smart_home["devices"][device_id])
    return Success({"error": "Устройство не найдено"})

@method
async def set_device_status(device_id, status):
    """Изменить статус устройства (on/off)"""
    if device_id in smart_home["devices"]:
        smart_home["devices"][device_id]["status"] = status
        return Success({"result": "success", "device": device_id, "status": status})
    return Success({"error": "Устройство не найдено"})

@method
async def set_light_brightness(device_id, brightness):
    """Установить яркость света (0-100%)"""
    if device_id in smart_home["devices"] and smart_home["devices"][device_id]["type"] == "light":
        if 0 <= brightness <= 100:
            smart_home["devices"][device_id]["brightness"] = brightness
            if brightness > 0:
                smart_home["devices"][device_id]["status"] = "on"
            else:
                smart_home["devices"][device_id]["status"] = "off"
            return Success({"result": "success", "device": device_id, "brightness": brightness})
        return Success({"error": "Яркость должна быть от 0 до 100"})
    return Success({"error": "Устройство не найдено или не является светильником"})

@method
async def set_temperature(temperature):
    """Установить целевую температуру термостата"""
    if 16 <= temperature <= 30:
        smart_home["devices"]["thermostat"]["temperature"] = temperature
        return Success({"result": "success", "temperature": temperature})
    return Success({"error": "Температура должна быть от 16 до 30 градусов"})

@method
async def activate_scene(scene_id):
    """Активировать сценарий умного дома"""
    if scene_id in smart_home["scenes"]:
        results = []
        if scene_id == "movie_night":
            # Настройка для просмотра фильма
            smart_home["devices"]["light_living_room"]["status"] = "on"
            smart_home["devices"]["light_living_room"]["brightness"] = 30
            smart_home["devices"]["tv"]["status"] = "on"
            smart_home["devices"]["tv"]["volume"] = 40
            results = ["Свет в гостиной приглушен", "Телевизор включен"]
        elif scene_id == "cooking":
            # Настройка для приготовления пищи
            smart_home["devices"]["light_kitchen"]["status"] = "on"
            smart_home["devices"]["light_kitchen"]["brightness"] = 100
            smart_home["devices"]["thermostat"]["temperature"] = 23
            results = ["Свет на кухне включен", "Температура установлена на 23°C"]
        elif scene_id == "away":
            # Настройка для режима "Никого нет дома"
            smart_home["devices"]["light_living_room"]["status"] = "off"
            smart_home["devices"]["light_kitchen"]["status"] = "off"
            smart_home["devices"]["tv"]["status"] = "off"
            smart_home["devices"]["door_lock"]["status"] = "locked"
            smart_home["devices"]["thermostat"]["temperature"] = 18
            results = ["Все освещение выключено", "Телевизор выключен", "Дверь заперта", "Температура снижена до 18°C"]
        
        return Success({"result": "success", "scene": scene_id, "actions": results})
    return Success({"error": "Сценарий не найден"})

@method
async def get_all_devices():
    """Получить список всех устройств и их статусы"""
    return Success(smart_home["devices"])

@method
async def get_sensors_data():
    """Получить данные с датчиков"""
    return Success(smart_home.get("sensors", {"error": "Датчики недоступны"}))

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
    
    # Запуск имитации датчиков
    asyncio.create_task(update_sensors())
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 5000)
    await site.start()
    print("Сервер запущен на http://localhost:5000/api")
    
    # Держим сервер запущенным
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_server())