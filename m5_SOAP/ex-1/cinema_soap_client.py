from zeep import Client
import datetime
from tabulate import tabulate

# URL SOAP сервиса
WSDL_URL = "http://127.0.0.1:8000/?wsdl"

# Создаем клиент
client = Client(WSDL_URL)

def print_movies(movies):
    """Вывод списка фильмов в табличном виде"""
    table_data = []
    for movie in movies:
        table_data.append([
            movie.id,
            movie.title,
            movie.genre,
            f"{movie.duration} мин.",
            movie.rating
        ])
    
    headers = ["ID", "Название", "Жанр", "Длительность", "Рейтинг"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def print_showtimes(showtimes):
    """Вывод списка сеансов в табличном виде"""
    table_data = []
    for showtime in showtimes:
        table_data.append([
            showtime.id,
            showtime.movie_title,
            showtime.date,
            showtime.time,
            f"Зал {showtime.hall}",
            f"{showtime.available_seats} мест",
            f"{showtime.price} руб."
        ])
    
    headers = ["ID", "Фильм", "Дата", "Время", "Зал", "Свободно", "Цена"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def print_ticket(ticket):
    """Вывод информации о билете"""
    if ticket.id == 0:
        print(f"\n⚠️ {ticket.movie_title}")
        return
    
    print("\n===== БИЛЕТ В КИНО =====")
    print(f"Фильм: {ticket.movie_title}")
    print(f"Дата: {ticket.date}")
    print(f"Время: {ticket.time}")
    print(f"Зал: {ticket.hall}")
    print(f"Место: {ticket.seat}")
    print(f"Цена: {ticket.price} руб.")
    print(f"Код бронирования: {ticket.booking_code}")
    print("=======================")

def main_menu():
    """Главное меню клиента"""
    while True:
        print("\n===== КИНОТЕАТР 'СИНЕМА SOAP' =====")
        print("1. Показать все фильмы")
        print("2. Показать все сеансы")
        print("3. Показать сеансы на сегодня")
        print("4. Показать сеансы для выбранного фильма")
        print("5. Забронировать билет")
        print("6. Проверить бронирование")
        print("7. Отменить бронирование")
        print("0. Выход")
        
        choice = input("\nВыберите опцию: ")
        
        if choice == "1":
            # Показать все фильмы
            movies = client.service.get_movies()
            print("\n--- СПИСОК ФИЛЬМОВ ---")
            print_movies(movies)
            
        elif choice == "2":
            # Показать все сеансы
            showtimes = client.service.get_all_showtimes()
            print("\n--- ВСЕ СЕАНСЫ ---")
            print_showtimes(showtimes)
            
        elif choice == "3":
            # Показать сеансы на сегодня
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            showtimes = client.service.get_showtimes_by_date(today)
            print(f"\n--- СЕАНСЫ НА СЕГОДНЯ ({today}) ---")
            print_showtimes(showtimes)
            
        elif choice == "4":
            # Показать сеансы для выбранного фильма
            movies = client.service.get_movies()
            print("\n--- СПИСОК ФИЛЬМОВ ---")
            print_movies(movies)
            
            movie_id = input("\nВведите ID фильма: ")
            try:
                movie_id = int(movie_id)
                showtimes = client.service.get_movie_showtimes(movie_id)
                movie = client.service.get_movie_details(movie_id)
                print(f"\n--- СЕАНСЫ ФИЛЬМА '{movie.title}' ---")
                print_showtimes(showtimes)
            except ValueError:
                print("Некорректный ID фильма")
            
        elif choice == "5":
            # Забронировать билет
            showtimes = client.service.get_all_showtimes()
            print("\n--- ДОСТУПНЫЕ СЕАНСЫ ---")
            print_showtimes(showtimes)
            
            try:
                showtime_id = int(input("\nВведите ID сеанса: "))
                seat_number = int(input("Введите номер места: "))
                
                ticket = client.service.book_ticket(showtime_id, seat_number)
                print_ticket(ticket)
                
                if ticket.id != 0:
                    print("\n✅ Билет успешно забронирован!")
                    print("Сохраните код бронирования для получения билета в кассе.")
            except ValueError:
                print("Некорректный ввод")
            
        elif choice == "6":
            # Проверить бронирование
            booking_code = input("\nВведите код бронирования: ")
            ticket = client.service.get_ticket_by_code(booking_code)
            print_ticket(ticket)
            
        elif choice == "7":
            # Отменить бронирование
            booking_code = input("\nВведите код бронирования для отмены: ")
            result = client.service.cancel_booking(booking_code)
            print(f"\n{result}")
            
        elif choice == "0":
            print("\nСпасибо за использование нашего сервиса! До свидания!")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"\nОшибка: {e}")
        print("Возможно, SOAP-сервер не запущен. Убедитесь, что сервер работает по адресу http://127.0.0.1:8000")