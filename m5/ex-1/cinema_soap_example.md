# Система бронирования билетов в кинотеатре с использованием SOAP API

Этот пример демонстрирует создание и использование SOAP API для системы бронирования билетов в кинотеатре. Пример показывает, как SOAP может использоваться для создания структурированного API с четко определенными типами данных и операциями.

## Особенности примера

- **Полноценная система бронирования** с фильмами, сеансами и билетами
- **Сложные типы данных** (ComplexModel) для структурированной передачи информации
- **Множество операций** для работы с разными аспектами системы
- **Валидация данных** на уровне SOAP-протокола
- **Интерактивный клиент** для демонстрации работы API

## Структура проекта

- `cinema_soap_server.py` - SOAP-сервер с реализацией API
- `cinema_soap_client.py` - клиент для взаимодействия с API
- `cinema_soap_example.md` - документация по примеру

## Запуск примера

1. Установите необходимые библиотеки:

   ```bash
   pip install spyne lxml zeep tabulate
   ```
2. Запустите SOAP-сервер:

   ```bash
   python cinema_soap_server.py
   ```
3. В другом терминале запустите клиент:

   ```bash
   python cinema_soap_client.py
   ```

winget install Python.Python.3.10

## Модели данных

### Movie (Фильм)

- `id` - уникальный идентификатор фильма
- `title` - название фильма
- `genre` - жанр фильма
- `duration` - продолжительность в минутах
- `rating` - возрастной рейтинг

### Showtime (Сеанс)

- `id` - уникальный идентификатор сеанса
- `movie_id` - идентификатор фильма
- `movie_title` - название фильма
- `date` - дата сеанса
- `time` - время начала сеанса
- `hall` - номер зала
- `available_seats` - количество доступных мест
- `price` - цена билета в рублях

### Ticket (Билет)

- `id` - уникальный идентификатор билета
- `showtime_id` - идентификатор сеанса
- `movie_title` - название фильма
- `date` - дата сеанса
- `time` - время сеанса
- `hall` - номер зала
- `seat` - номер места
- `price` - цена билета
- `booking_code` - уникальный код бронирования

## Операции SOAP API

### Работа с фильмами

- `get_movies()` - получить список всех фильмов
- `get_movie_details(movie_id)` - получить детальную информацию о фильме по ID

### Работа с сеансами

- `get_all_showtimes()` - получить список всех сеансов
- `get_movie_showtimes(movie_id)` - получить список сеансов для конкретного фильма
- `get_showtimes_by_date(date)` - получить список сеансов на определенную дату

### Работа с билетами

- `book_ticket(showtime_id, seat_number)` - забронировать билет на сеанс
- `get_ticket_by_code(booking_code)` - получить информацию о билете по коду бронирования
- `cancel_booking(booking_code)` - отменить бронирование билета

## Пример SOAP-запроса (XML)

Запрос на бронирование билета:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cin="http://cinema.example.com/soap">
   <soapenv:Header/>
   <soapenv:Body>
      <cin:book_ticket>
         <cin:showtime_id>1</cin:showtime_id>
         <cin:seat_number>15</cin:seat_number>
      </cin:book_ticket>
   </soapenv:Body>
</soapenv:Envelope>
```

Ответ:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <ns0:book_ticketResponse xmlns:ns0="http://cinema.example.com/soap">
         <ns0:book_ticketResult>
            <ns0:id>1</ns0:id>
            <ns0:showtime_id>1</ns0:showtime_id>
            <ns0:movie_title>Матрица</ns0:movie_title>
            <ns0:date>2023-05-15</ns0:date>
            <ns0:time>10:00</ns0:time>
            <ns0:hall>1</ns0:hall>
            <ns0:seat>15</ns0:seat>
            <ns0:price>250</ns0:price>
            <ns0:booking_code>TKT-1-15-1</ns0:booking_code>
         </ns0:book_ticketResult>
      </ns0:book_ticketResponse>
   </soapenv:Body>
</soapenv:Envelope>
```

## Преимущества использования SOAP для данного примера

1. **Строгая типизация данных** - гарантирует корректность передаваемых данных
2. **Самодокументируемость** - WSDL-файл автоматически описывает все доступные операции
3. **Транзакционность** - подходит для финансовых операций (бронирование, оплата)
4. **Стандартизация** - совместимость с корпоративными системами
5. **Расширяемость** - легко добавлять новые операции и типы данных

## Возможные улучшения

- Добавление аутентификации и авторизации пользователей
- Интеграция с платежной системой
- Добавление системы скидок и промокодов
- Расширение функциональности для администраторов кинотеатра
- Добавление уведомлений о бронировании по email/SMS
