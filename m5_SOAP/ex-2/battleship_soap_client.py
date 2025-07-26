from zeep import Client
import os
import platform

# URL SOAP сервиса
WSDL_URL = "http://127.0.0.1:8000/?wsdl"

# Создаем клиент
client = Client(WSDL_URL)

# Текущая игра
current_game = None

def clear_screen():
    """Очистка экрана в зависимости от ОС"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def print_board(board, is_player_board):
    """Отображение игрового поля"""
    # Заголовок
    if is_player_board:
        print("\n=== ВАШЕ ПОЛЕ ===")
    else:
        print("\n=== ПОЛЕ КОМПЬЮТЕРА ===")
    
    # Верхняя строка с номерами столбцов
    print("   ", end="")
    for x in range(10):
        print(f" {x} ", end="")
    print()
    
    # Игровое поле
    for y in range(10):
        print(f" {y} ", end="")
        
        for x in range(10):
            # Проверяем, был ли выстрел в эту клетку
            shot_here = False
            for shot in board.shots:
                if shot.x == x and shot.y == y:
                    shot_here = True
                    break
            
            # Проверяем, есть ли здесь корабль
            ship_here = None
            for ship in board.ships:
                for coord in ship.coordinates:
                    if coord.x == x and coord.y == y:
                        ship_here = ship
                        break
                if ship_here:
                    break
            
            # Отображаем символ в зависимости от состояния клетки
            if shot_here and ship_here:
                print(" X ", end="")  # Попадание
            elif shot_here:
                print(" · ", end="")  # Промах
            elif is_player_board and ship_here:
                print(" O ", end="")  # Корабль игрока
            else:
                print(" ~ ", end="")  # Пустая клетка или скрытый корабль компьютера
        
        print()  # Переход на новую строку

def display_game_state(game_state):
    """Отображение текущего состояния игры"""
    clear_screen()
    
    print("\n===== МОРСКОЙ БОЙ =====")
    print(f"ID игры: {game_state.game_id}")
    
    # Отображаем поля
    print_board(game_state.player_board, True)
    print_board(game_state.computer_board, False)
    
    # Отображаем сообщение
    print(f"\nСообщение: {game_state.message}")
    
    # Отображаем статус игры
    if game_state.game_over:
        if game_state.winner == "player":
            print("\n🎉 ВЫ ПОБЕДИЛИ! 🎉")
        else:
            print("\n😢 ВЫ ПРОИГРАЛИ 😢")
    else:
        if game_state.player_turn:
            print("\nВаш ход!")
        else:
            print("\nХод компьютера...")

def main_menu():
    """Главное меню игры"""
    global current_game
    
    while True:
        clear_screen()
        print("\n===== МОРСКОЙ БОЙ =====")
        print("1. Новая игра")
        print("2. Продолжить текущую игру")
        print("0. Выход")
        
        choice = input("\nВыберите опцию: ")
        
        if choice == "1":
            try:
                # Создаем новую игру
                current_game = client.service.new_game()
                play_game()
            except Exception as e:
                print(f"\nОшибка: {e}")
                print("Возможно, SOAP-сервер не запущен. Убедитесь, что сервер работает по адресу http://127.0.0.1:8000")
                input("\nНажмите Enter для продолжения...")
        
        elif choice == "2":
            if current_game and current_game.game_id:
                try:
                    # Получаем актуальное состояние игры
                    current_game = client.service.get_game_state(current_game.game_id)
                    if current_game.game_id:
                        play_game()
                    else:
                        print("\nИгра не найдена. Начните новую игру.")
                        input("\nНажмите Enter для продолжения...")
                except Exception as e:
                    print(f"\nОшибка: {e}")
                    input("\nНажмите Enter для продолжения...")
            else:
                print("\nНет активной игры. Начните новую игру.")
                input("\nНажмите Enter для продолжения...")
        
        elif choice == "0":
            print("\nСпасибо за игру! До свидания!")
            break
        
        else:
            print("\nНеверный выбор. Попробуйте снова.")
            input("\nНажмите Enter для продолжения...")

def play_game():
    """Игровой процесс"""
    global current_game
    
    while True:
        # Отображаем текущее состояние игры
        display_game_state(current_game)
        
        # Если игра закончена, выходим
        if current_game.game_over:
            input("\nНажмите Enter для возврата в главное меню...")
            break
        
        # Если ход игрока, запрашиваем координаты выстрела
        if current_game.player_turn:
            try:
                print("\nВведите координаты выстрела (x y):")
                coords = input("> ").split()
                
                if len(coords) != 2:
                    print("\nНекорректный ввод. Введите два числа, разделенных пробелом.")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                x = int(coords[0])
                y = int(coords[1])
                
                if x < 0 or x >= 10 or y < 0 or y >= 10:
                    print("\nКоординаты должны быть в диапазоне от 0 до 9.")
                    input("\nНажмите Enter для продолжения...")
                    continue
                
                # Делаем выстрел
                current_game = client.service.player_shot(current_game.game_id, x, y)
                
            except ValueError:
                print("\nНекорректный ввод. Введите два числа.")
                input("\nНажмите Enter для продолжения...")
            except Exception as e:
                print(f"\nОшибка: {e}")
                input("\nНажмите Enter для продолжения...")
        else:
            # Если ход компьютера, просто обновляем состояние игры
            input("\nНажмите Enter для хода компьютера...")
            current_game = client.service.get_game_state(current_game.game_id)

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"\nОшибка: {e}")
        print("Возможно, SOAP-сервер не запущен. Убедитесь, что сервер работает по адресу http://127.0.0.1:8000")