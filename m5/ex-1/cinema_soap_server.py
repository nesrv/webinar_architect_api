from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import datetime

# Модели данных
class Movie(ComplexModel):
    """Модель фильма"""
    id = Integer
    title = Unicode
    genre = Unicode
    duration = Integer  # в минутах
    rating = Unicode

class Showtime(ComplexModel):
    """Модель сеанса"""
    id = Integer
    movie_id = Integer
    movie_title = Unicode
    date = Unicode
    time = Unicode
    hall = Integer
    available_seats = Integer
    price = Integer  # в рублях

class Ticket(ComplexModel):
    """Модель билета"""
    id = Integer
    showtime_id = Integer
    movie_title = Unicode
    date = Unicode
    time = Unicode
    hall = Integer
    seat = Integer
    price = Integer
    booking_code = Unicode

# База данных (имитация)
movies_db = {
    1: {"id": 1, "title": "Матрица", "genre": "Фантастика", "duration": 136, "rating": "16+"},
    2: {"id": 2, "title": "Интерстеллар", "genre": "Фантастика", "duration": 169, "rating": "12+"},
    3: {"id": 3, "title": "Начало", "genre": "Фантастика", "duration": 148, "rating": "12+"},
    4: {"id": 4, "title": "Зеленая миля", "genre": "Драма", "duration": 189, "rating": "16+"},
    5: {"id": 5, "title": "Гладиатор", "genre": "Исторический", "duration": 155, "rating": "16+"}
}

# Генерация сеансов на ближайшие 3 дня
showtimes_db = {}
showtime_id = 1

for movie_id, movie in movies_db.items():
    for day in range(3):  # на 3 дня вперед
        date = (datetime.datetime.now() + datetime.timedelta(days=day)).strftime("%Y-%m-%d")
        
        # Утренний сеанс
        showtimes_db[showtime_id] = {
            "id": showtime_id,
            "movie_id": movie_id,
            "movie_title": movie["title"],
            "date": date,
            "time": "10:00",
            "hall": 1,
            "available_seats": 50,
            "price": 250
        }
        showtime_id += 1
        
        # Дневной сеанс
        showtimes_db[showtime_id] = {
            "id": showtime_id,
            "movie_id": movie_id,
            "movie_title": movie["title"],
            "date": date,
            "time": "15:00",
            "hall": 2,
            "available_seats": 70,
            "price": 350
        }
        showtime_id += 1
        
        # Вечерний сеанс
        showtimes_db[showtime_id] = {
            "id": showtime_id,
            "movie_id": movie_id,
            "movie_title": movie["title"],
            "date": date,
            "time": "20:00",
            "hall": 3,
            "available_seats": 100,
            "price": 450
        }
        showtime_id += 1

# Билеты
tickets_db = {}
ticket_id = 1

# SOAP сервис
class CinemaService(ServiceBase):
    """Сервис бронирования билетов в кинотеатре"""
    
    @rpc(_returns=Iterable(Movie))
    def get_movies(ctx):
        """Получить список всех фильмов"""
        for movie_id, movie_data in movies_db.items():
            yield Movie(**movie_data)
    
    @rpc(Integer, _returns=Movie)
    def get_movie_details(ctx, movie_id):
        """Получить детальную информацию о фильме по ID"""
        if movie_id in movies_db:
            return Movie(**movies_db[movie_id])
        return Movie(id=0, title="Фильм не найден", genre="", duration=0, rating="")
    
    @rpc(_returns=Iterable(Showtime))
    def get_all_showtimes(ctx):
        """Получить список всех сеансов"""
        for showtime_id, showtime_data in showtimes_db.items():
            yield Showtime(**showtime_data)
    
    @rpc(Integer, _returns=Iterable(Showtime))
    def get_movie_showtimes(ctx, movie_id):
        """Получить список сеансов для конкретного фильма"""
        for showtime_id, showtime_data in showtimes_db.items():
            if showtime_data["movie_id"] == movie_id:
                yield Showtime(**showtime_data)
    
    @rpc(Unicode, _returns=Iterable(Showtime))
    def get_showtimes_by_date(ctx, date):
        """Получить список сеансов на определенную дату"""
        for showtime_id, showtime_data in showtimes_db.items():
            if showtime_data["date"] == date:
                yield Showtime(**showtime_data)
    
    @rpc(Integer, Integer, _returns=Ticket)
    def book_ticket(ctx, showtime_id, seat_number):
        """Забронировать билет на сеанс"""
        global ticket_id
        
        if showtime_id not in showtimes_db:
            return Ticket(id=0, showtime_id=0, movie_title="Сеанс не найден", 
                         date="", time="", hall=0, seat=0, price=0, booking_code="ERROR")
        
        showtime = showtimes_db[showtime_id]
        
        # Проверяем наличие свободных мест
        if showtime["available_seats"] <= 0:
            return Ticket(id=0, showtime_id=0, movie_title="Нет свободных мест", 
                         date="", time="", hall=0, seat=0, price=0, booking_code="FULL")
        
        # Проверяем, не занято ли уже это место
        for ticket in tickets_db.values():
            if ticket["showtime_id"] == showtime_id and ticket["seat"] == seat_number:
                return Ticket(id=0, showtime_id=0, movie_title="Место уже занято", 
                             date="", time="", hall=0, seat=0, price=0, booking_code="TAKEN")
        
        # Генерируем уникальный код бронирования
        booking_code = f"TKT-{showtime_id}-{seat_number}-{ticket_id}"
        
        # Создаем билет
        ticket = {
            "id": ticket_id,
            "showtime_id": showtime_id,
            "movie_title": showtime["movie_title"],
            "date": showtime["date"],
            "time": showtime["time"],
            "hall": showtime["hall"],
            "seat": seat_number,
            "price": showtime["price"],
            "booking_code": booking_code
        }
        
        tickets_db[ticket_id] = ticket
        ticket_id += 1
        
        # Уменьшаем количество доступных мест
        showtimes_db[showtime_id]["available_seats"] -= 1
        
        return Ticket(**ticket)
    
    @rpc(Unicode, _returns=Ticket)
    def get_ticket_by_code(ctx, booking_code):
        """Получить информацию о билете по коду бронирования"""
        for ticket_id, ticket_data in tickets_db.items():
            if ticket_data["booking_code"] == booking_code:
                return Ticket(**ticket_data)
        
        return Ticket(id=0, showtime_id=0, movie_title="Билет не найден", 
                     date="", time="", hall=0, seat=0, price=0, booking_code="NOT_FOUND")
    
    @rpc(Unicode, _returns=Unicode)
    def cancel_booking(ctx, booking_code):
        """Отменить бронирование билета"""
        for ticket_id, ticket_data in list(tickets_db.items()):
            if ticket_data["booking_code"] == booking_code:
                # Возвращаем место в пул доступных
                showtime_id = ticket_data["showtime_id"]
                showtimes_db[showtime_id]["available_seats"] += 1
                
                # Удаляем билет
                del tickets_db[ticket_id]
                
                return "Бронирование успешно отменено"
        
        return "Билет с указанным кодом не найден"

# Создаем приложение
application = Application(
    [CinemaService],
    tns='http://cinema.example.com/soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Создаем WSGI приложение
wsgi_app = WsgiApplication(application)

# Запускаем сервер
if __name__ == '__main__':
    server = make_server('127.0.0.1', 8000, wsgi_app)
    print("SOAP сервер запущен на http://127.0.0.1:8000")
    print("WSDL доступен по адресу: http://127.0.0.1:8000/?wsdl")
    server.serve_forever()