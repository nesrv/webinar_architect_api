# Как работает SOAP в cinema_soap_server.py

## Архитектура SOAP сервиса

### 1. Импорты и настройка
```python
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
```

**Spyne** - Python библиотека для создания SOAP веб-сервисов:
- `ServiceBase` - базовый класс для SOAP сервиса
- `@rpc` - декоратор для создания SOAP методов
- `Soap11` - протокол SOAP версии 1.1
- `ComplexModel` - для создания сложных типов данных

### 2. Модели данных (ComplexModel)

```python
class Movie(ComplexModel):
    id = Integer
    title = Unicode
    genre = Unicode
    duration = Integer
    rating = Unicode
```

**ComplexModel** создает XML Schema типы:
- Автоматически генерируется WSDL
- Валидация входящих/исходящих данных
- Сериализация Python объектов в XML

### 3. SOAP сервис класс

```python
class CinemaService(ServiceBase):
    @rpc(_returns=Iterable(Movie))
    def get_movies(ctx):
        # Возвращает список фильмов
```

**@rpc декоратор**:
- Превращает Python метод в SOAP операцию
- `_returns` - определяет тип возвращаемых данных
- `ctx` - контекст SOAP запроса (обязательный параметр)

### 4. Типы SOAP операций в сервисе

#### Простой запрос без параметров:
```python
@rpc(_returns=Iterable(Movie))
def get_movies(ctx):
    # Возвращает все фильмы
```

#### Запрос с параметрами:
```python
@rpc(Integer, _returns=Movie)
def get_movie_details(ctx, movie_id):
    # Возвращает фильм по ID
```

#### Сложная операция с несколькими параметрами:
```python
@rpc(Integer, Integer, _returns=Ticket)
def book_ticket(ctx, showtime_id, seat_number):
    # Бронирует билет
```

### 5. Создание SOAP приложения

```python
application = Application(
    [CinemaService],                    # Список сервисов
    tns='http://cinema.example.com/soap', # Target namespace
    in_protocol=Soap11(validator='lxml'), # Входящий протокол
    out_protocol=Soap11()               # Исходящий протокол
)
```

**Application** объединяет:
- Сервисы в единое SOAP приложение
- Генерирует WSDL автоматически
- Обрабатывает SOAP envelope

### 6. WSGI интеграция

```python
wsgi_app = WsgiApplication(application)
server = make_server('127.0.0.1', 8000, wsgi_app)
```

**WsgiApplication**:
- Интегрирует SOAP с WSGI
- Обрабатывает HTTP запросы
- Парсит SOAP XML в Python объекты

## Как происходит обработка SOAP запроса

### 1. Клиент отправляет SOAP запрос:
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <get_movie_details>
            <movie_id>1</movie_id>
        </get_movie_details>
    </soap:Body>
</soap:Envelope>
```

### 2. Spyne автоматически:
- Парсит XML в Python объекты
- Валидирует типы данных
- Вызывает соответствующий метод
- Сериализует результат обратно в XML

### 3. Сервер возвращает SOAP ответ:
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <get_movie_detailsResponse>
            <get_movie_detailsResult>
                <id>1</id>
                <title>Матрица</title>
                <genre>Фантастика</genre>
                <duration>136</duration>
                <rating>16+</rating>
            </get_movie_detailsResult>
        </get_movie_detailsResponse>
    </soap:Body>
</soap:Envelope>
```

## Особенности реализации

### Управление состоянием:
- Глобальные переменные (`movies_db`, `tickets_db`) имитируют базу данных
- Состояние сохраняется между запросами в памяти сервера

### Обработка ошибок:
- Возврат объектов с "ошибочными" значениями (id=0, booking_code="ERROR")
- В реальном проекте лучше использовать SOAP Fault

### WSDL генерация:
- Автоматически доступен по адресу `http://127.0.0.1:8000/?wsdl`
- Описывает все доступные операции и типы данных

## Запуск и тестирование

1. **Запуск сервера:**
   ```bash
   python cinema_soap_server.py
   ```

2. **Просмотр WSDL:**
   ```
   http://127.0.0.1:8000/?wsdl
   ```

## Тестирование в Postman

### Настройка запроса:
1. **Method:** POST
2. **URL:** `http://127.0.0.1:8000`
3. **Headers:**
   - `Content-Type: text/xml; charset=utf-8`
   - `SOAPAction: "get_movies"` (название метода)

### Примеры SOAP запросов:

#### 1. Получить все фильмы:
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <tns:get_movies xmlns:tns="http://cinema.example.com/soap" />
    </soap:Body>
</soap:Envelope>
```

#### 2. Получить фильм по ID:
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <tns:get_movie_details xmlns:tns="http://cinema.example.com/soap">
            <tns:movie_id>1</tns:movie_id>
        </tns:get_movie_details>
    </soap:Body>
</soap:Envelope>
```

#### 3. Получить все сеансы:
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <tns:get_all_showtimes xmlns:tns="http://cinema.example.com/soap" />
    </soap:Body>
</soap:Envelope>
```

#### 4. Забронировать билет:
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <tns:book_ticket xmlns:tns="http://cinema.example.com/soap">
            <tns:showtime_id>1</tns:showtime_id>
            <tns:seat_number>15</tns:seat_number>
        </tns:book_ticket>
    </soap:Body>
</soap:Envelope>
```

#### 5. Получить билет по коду:
```xml
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <tns:get_ticket_by_code xmlns:tns="http://cinema.example.com/soap">
            <tns:booking_code>TKT-1-15-1</tns:booking_code>
        </tns:get_ticket_by_code>
    </soap:Body>
</soap:Envelope>
```

### Важные моменты для Postman:
- Используйте **Body → raw → XML**
- Обязательно укажите `Content-Type: text/xml`
- SOAPAction заголовок должен соответствовать методу
- Namespace `tns` должен совпадать с `http://cinema.example.com/soap`

### Ожидаемый формат ответа:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/">
    <soap11env:Body>
        <tns:get_moviesResponse xmlns:tns="http://cinema.example.com/soap">
            <tns:get_moviesResult>
                <tns:Movie>
                    <tns:id>1</tns:id>
                    <tns:title>Матрица</tns:title>
                    <tns:genre>Фантастика</tns:genre>
                    <tns:duration>136</tns:duration>
                    <tns:rating>16+</tns:rating>
                </tns:Movie>
            </tns:get_moviesResult>
        </tns:get_moviesResponse>
    </soap11env:Body>
</soap11env:Envelope>
```