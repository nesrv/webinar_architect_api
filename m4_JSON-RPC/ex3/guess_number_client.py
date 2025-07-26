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
        result = response["result"]
        
        # Проверяем наличие сообщения об ошибке
        if "error" in result:
            print(f"\n❌ {result['error']}")
            if "message" in result:
                print(f"ℹ️ {result['message']}")
            return
        
        # Выводим сообщение, если оно есть
        if "message" in result:
            print(f"\n✉️ {result['message']}")
        
        # Выводим подсказку, если она есть
        if "hint" in result:
            print(f"\n💡 Подсказка: {result['hint']}")
        
        # Выводим количество попыток, если оно есть
        if "attempts" in result:
            print(f"🔢 Попыток: {result['attempts']}")
        
        # Выводим ID игры, если он есть
        if "game_id" in result:
            print(f"🎮 ID игры: {result['game_id']}")
            
        # Выводим сложность, если она есть
        if "difficulty" in result:
            difficulties = {
                "easy": "Легкая",
                "normal": "Нормальная",
                "hard": "Сложная"
            }
            print(f"⚙️ Сложность: {difficulties.get(result['difficulty'], result['difficulty'])}")
            
        # Выводим историю попыток, если она есть
        if "history" in result:
            if result["history"]:
                print(f"\n📜 История попыток: {', '.join(map(str, result['history']))}")
            else:
                print("\n📜 История попыток пуста")
    else:
        print("\n❌ Ошибка:")
        print(json.dumps(response.get("error", "Неизвестная ошибка"), indent=2, ensure_ascii=False))

def main_menu():
    """Главное меню игры"""
    current_game = None
    
    while True:
        print("\n===== ИГРА 'УГАДАЙ ЧИСЛО' =====")
        
        if current_game:
            print(f"🎮 Текущая игра: {current_game}")
            print("\n1. Сделать попытку")
            print("2. Получить подсказку")
            print("3. Посмотреть статистику")
            print("4. Сдаться")
            print("5. Начать новую игру")
            print("0. Выход")
        else:
            print("\n1. Начать новую игру")
            print("0. Выход")
        
        choice = input("\nВыберите опцию: ")
        
        if not current_game and choice == "1":
            # Начать новую игру
            print("\n--- Выберите сложность ---")
            print("1. Легкая (1-50)")
            print("2. Нормальная (1-100)")
            print("3. Сложная (1-200)")
            
            difficulty_choice = input("Выберите сложность: ")
            
            if difficulty_choice == "1":
                difficulty = "easy"
            elif difficulty_choice == "2":
                difficulty = "normal"
            elif difficulty_choice == "3":
                difficulty = "hard"
            else:
                print("Неверный выбор, используется нормальная сложность")
                difficulty = "normal"
                
            response = call_method("start_game", {"difficulty": difficulty})
            print_response(response)
            
            if "result" in response and "game_id" in response["result"]:
                current_game = response["result"]["game_id"]
                
        elif current_game and choice == "1":
            # Сделать попытку
            try:
                guess = int(input("\nВведите число: "))
                response = call_method("guess", {"game_id": current_game, "number": guess})
                print_response(response)
                
                # Проверяем, не закончилась ли игра
                if "result" in response and "status" in response["result"] and response["result"]["status"] == "won":
                    print("\n🎉 Поздравляем! Вы выиграли!")
                    play_again = input("\nХотите сыграть еще раз? (да/нет): ")
                    if play_again.lower() in ["да", "д", "yes", "y"]:
                        current_game = None
                    else:
                        return
            except ValueError:
                print("Пожалуйста, введите корректное число")
                
        elif current_game and choice == "2":
            # Получить подсказку
            response = call_method("get_hint", {"game_id": current_game})
            print_response(response)
            
        elif current_game and choice == "3":
            # Посмотреть статистику
            response = call_method("game_stats", {"game_id": current_game})
            print_response(response)
            
        elif current_game and choice == "4":
            # Сдаться
            response = call_method("give_up", {"game_id": current_game})
            print_response(response)
            
            play_again = input("\nХотите сыграть еще раз? (да/нет): ")
            if play_again.lower() in ["да", "д", "yes", "y"]:
                current_game = None
            else:
                return
                
        elif (current_game and choice == "5") or (not current_game and choice == "1"):
            # Начать новую игру
            print("\n--- Выберите сложность ---")
            print("1. Легкая (1-50)")
            print("2. Нормальная (1-100)")
            print("3. Сложная (1-200)")
            
            difficulty_choice = input("Выберите сложность: ")
            
            if difficulty_choice == "1":
                difficulty = "easy"
            elif difficulty_choice == "2":
                difficulty = "normal"
            elif difficulty_choice == "3":
                difficulty = "hard"
            else:
                print("Неверный выбор, используется нормальная сложность")
                difficulty = "normal"
                
            response = call_method("start_game", {"difficulty": difficulty})
            print_response(response)
            
            if "result" in response and "game_id" in response["result"]:
                current_game = response["result"]["game_id"]
            
        elif choice == "0":
            print("Спасибо за игру! До свидания!")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()