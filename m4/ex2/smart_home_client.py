import requests
import json

# URL JSON-RPC API
API_URL = "http://localhost:5000/api"

def call_method(method, params=None):
    """Вызов метода JSON-RPC API"""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": 1
    }
    
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()

def print_response(response):
    """Красивый вывод ответа"""
    if "result" in response:
        print("\nРезультат:")
        print(json.dumps(response["result"], indent=2, ensure_ascii=False))
    else:
        print("\nОшибка:")
        print(json.dumps(response.get("error", "Неизвестная ошибка"), indent=2, ensure_ascii=False))

def main_menu():
    """Главное меню клиента умного дома"""
    while True:
        print("\n===== Система управления умным домом =====")
        print("1. Показать все устройства")
        print("2. Управление освещением")
        print("3. Управление термостатом")
        print("4. Активировать сценарий")
        print("5. Данные с датчиков")
        print("0. Выход")
        
        choice = input("\nВыберите опцию: ")
        
        if choice == "1":
            # Получить список всех устройств
            response = call_method("get_all_devices")
            print_response(response)
            
        elif choice == "2":
            # Меню управления освещением
            print("\n--- Управление освещением ---")
            print("1. Гостиная")
            print("2. Кухня")
            light_choice = input("Выберите комнату: ")
            
            if light_choice == "1":
                device_id = "light_living_room"
                room = "гостиной"
            elif light_choice == "2":
                device_id = "light_kitchen"
                room = "кухне"
            else:
                print("Неверный выбор")
                continue
                
            print(f"\nУправление светом в {room}")
            print("1. Включить")
            print("2. Выключить")
            print("3. Установить яркость")
            action = input("Выберите действие: ")
            
            if action == "1":
                response = call_method("set_device_status", {"device_id": device_id, "status": "on"})
                print_response(response)
            elif action == "2":
                response = call_method("set_device_status", {"device_id": device_id, "status": "off"})
                print_response(response)
            elif action == "3":
                brightness = int(input("Введите яркость (0-100): "))
                response = call_method("set_light_brightness", {"device_id": device_id, "brightness": brightness})
                print_response(response)
                
        elif choice == "3":
            # Управление термостатом
            print("\n--- Управление термостатом ---")
            print("Текущая температура:")
            response = call_method("get_device_status", {"device_id": "thermostat"})
            print_response(response)
            
            temp = float(input("\nУстановить новую температуру (16-30): "))
            response = call_method("set_temperature", {"temperature": temp})
            print_response(response)
            
        elif choice == "4":
            # Активация сценария
            print("\n--- Сценарии ---")
            print("1. Просмотр фильма")
            print("2. Приготовление пищи")
            print("3. Никого нет дома")
            
            scene_choice = input("Выберите сценарий: ")
            
            if scene_choice == "1":
                scene_id = "movie_night"
            elif scene_choice == "2":
                scene_id = "cooking"
            elif scene_choice == "3":
                scene_id = "away"
            else:
                print("Неверный выбор")
                continue
                
            response = call_method("activate_scene", {"scene_id": scene_id})
            print_response(response)
            
        elif choice == "5":
            # Данные с датчиков
            response = call_method("get_sensors_data")
            print_response(response)
            
        elif choice == "0":
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()