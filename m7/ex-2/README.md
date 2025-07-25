# Пример gRPC API для сервиса прогноза погоды

Этот проект демонстрирует создание и использование gRPC API для сервиса прогноза погоды. Пример включает в себя различные типы взаимодействий: унарные запросы, серверный стриминг, клиентский стриминг и двунаправленный стриминг.

## Структура проекта

- `weather.proto` - определение сервиса и сообщений в формате Protocol Buffers
- `generate_grpc.bat` - скрипт для генерации кода из proto-файла
- `weather_server.py` - реализация сервера gRPC
- `weather_client.py` - клиент для взаимодействия с сервером
- `README.md` - документация проекта

## Установка зависимостей

```bash
pip install grpcio grpcio-tools
python -m pip install  grpcio grpcio-tools
```

## Генерация кода из proto-файла

Запустите скрипт `generate_grpc.bat` или выполните следующую команду:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. weather.proto
```

Это создаст два файла:

- `weather_pb2.py` - содержит классы сообщений
- `weather_pb2_grpc.py` - содержит классы клиента и сервера

## Запуск сервера

```bash
python weather_server.py
```

Сервер запустится на порту 50051.

## Запуск клиента

```bash
python weather_client.py
```

Клиент предоставляет интерактивное меню для взаимодействия с сервером.

## Функциональность API

### 1. Унарные запросы (Unary RPC)

- **GetCurrentWeather** - получение текущей погоды по городу
- **GetForecast** - получение прогноза погоды на несколько дней

### 2. Серверный стриминг (Server Streaming RPC)

- **SubscribeToWeatherUpdates** - подписка на обновления погоды в реальном времени

### 3. Клиентский стриминг (Client Streaming RPC)

- **SendWeatherData** - отправка данных с метеостанции на сервер

### 4. Двунаправленный стриминг (Bidirectional Streaming RPC)

- **ChatWithMeteorologist** - чат с метеорологом в реальном времени

## Модели данных

- **CityRequest** - запрос погоды по городу
- **WeatherResponse** - ответ с текущей погодой
- **ForecastRequest** - запрос прогноза погоды
- **ForecastResponse** - ответ с прогнозом погоды
- **DailyForecast** - прогноз на один день
- **WeatherData** - данные с метеостанции
- **DataResponse** - ответ на отправку данных
- **ChatMessage** - сообщение для чата с метеорологом

## Преимущества использования gRPC для данного примера

1. **Эффективная сериализация** - Protocol Buffers обеспечивают компактное бинарное представление данных
2. **Строгая типизация** - четкое определение интерфейса API
3. **Поддержка стриминга** - возможность передачи потоковых данных в реальном времени
4. **Двунаправленная связь** - удобно для реализации чата и подписок на обновления
5. **Высокая производительность** - оптимизированный протокол HTTP/2

## Тестирование gRPC API в Postman

### Настройка Postman для gRPC

1. **Создайте новый gRPC запрос:**
   - New → gRPC Request
   - Server URL: `localhost:50051`

2. **Импорт proto файла:**
   - Import → Proto file
   - Выберите файл `weather.proto`
   - Или скопируйте содержимое в Proto definition

### Примеры тестирования методов

#### 1. GetCurrentWeather (Unary)
- **Service:** `WeatherService`
- **Method:** `GetCurrentWeather`
- **Message:**
```json
{
  "city": "Москва"
}
```

#### 2. GetForecast (Unary)
- **Service:** `WeatherService`
- **Method:** `GetForecast`
- **Message:**
```json
{
  "city": "Санкт-Петербург",
  "days": 5
}
```

#### 3. SubscribeToWeatherUpdates (Server Streaming)
- **Service:** `WeatherService`
- **Method:** `SubscribeToWeatherUpdates`
- **Message:**
```json
{
  "city": "Екатеринбург"
}
```
- Получите поток обновлений в реальном времени

#### 4. SendWeatherData (Client Streaming)
- **Service:** `WeatherService`
- **Method:** `SendWeatherData`
- **Messages:** (отправьте несколько сообщений)
```json
{
  "station_id": "MSK001",
  "temperature": 25.5,
  "humidity": 60,
  "pressure": 1013.25,
  "wind_speed": 5.2
}
```
```json
{
  "station_id": "MSK001",
  "temperature": 26.0,
  "humidity": 58,
  "pressure": 1012.8,
  "wind_speed": 4.8
}
```

#### 5. ChatWithMeteorologist (Bidirectional Streaming)
- **Service:** `WeatherService`
- **Method:** `ChatWithMeteorologist`
- **Messages:**
```json
{
  "user": "client",
  "message": "Привет! Какая погода ожидается завтра?"
}
```
```json
{
  "user": "client",
  "message": "Спасибо за информацию!"
}
```

### Важные моменты для Postman:

1. **Убедитесь, что сервер запущен** на `localhost:50051`
2. **Proto файл должен быть корректно импортирован**
3. **Для streaming методов** используйте кнопки Start/Stop streaming
4. **Client streaming:** отправляйте несколько сообщений через "Send message"
5. **Bidirectional streaming:** можете отправлять и получать сообщения одновременно

### Альтернативные инструменты:

- **grpcurl** - CLI инструмент для тестирования gRPC
- **BloomRPC** - GUI клиент для gRPC
- **Evans** - интерактивный gRPC клиент

## Возможные улучшения

- Добавление аутентификации и авторизации
- Интеграция с реальным API прогноза погоды
- Реализация кэширования данных
- Добавление обработки ошибок и повторных попыток
- Реализация TLS для безопасного соединения
