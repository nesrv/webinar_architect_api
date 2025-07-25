# JSON-RPC API - Учебная документация

## Описание
JSON-RPC - это протокол удаленного вызова процедур (RPC), использующий JSON для кодирования данных. Простой и легковесный протокол для взаимодействия клиент-сервер.

## Структура проекта
```
m4/ex1/
├── server.py           # Базовый JSON-RPC сервер (только POST)
├── server_with_get.py  # Расширенный сервер (POST + GET)
└── client.py           # Клиент для тестирования
```

## Запуск

### 1. Установка зависимостей
```bash
pip install aiohttp jsonrpcserver jsonrpcclient
```

### 2. Запуск сервера
```bash
# Базовый сервер
python server.py

# Или расширенный сервер
python server_with_get.py
```

### 3. Тестирование клиента
```bash
python client.py
```

## API методы

### add(a, b)
Складывает два числа
- **Параметры**: `a` (число), `b` (число)
- **Возвращает**: сумма чисел

### get_user(user_id)
Получает информацию о пользователе
- **Параметры**: `user_id` (число)
- **Возвращает**: объект с `id` и `name`

## Примеры запросов

### POST запрос (стандартный JSON-RPC)
```bash
curl -X POST http://localhost:5000/rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 1}'
```

**Ответ:**
```json
{"jsonrpc": "2.0", "result": 5, "id": 1}
```

### GET запрос (только server_with_get.py)
```bash
# Метод add
curl "http://localhost:5000/rpc?method=add&params[]=2&params[]=3&id=1"

# Метод get_user
curl "http://localhost:5000/rpc?method=get_user&params[]=2&id=2"
```

## Формат JSON-RPC 2.0

### Запрос
```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": [param1, param2],
  "id": 1
}
```

### Успешный ответ
```json
{
  "jsonrpc": "2.0",
  "result": "result_value",
  "id": 1
}
```

### Ответ с ошибкой
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 1
}
```

## Особенности реализации

### server.py
- Только POST запросы
- Стандартная реализация JSON-RPC
- Порт: 5000

### server_with_get.py
- POST и GET запросы
- GET параметры конвертируются в JSON-RPC формат
- Поддержка массивов через `params[]`

### client.py
- Демонстрация создания запросов
- Парсинг ответов
- Примеры использования библиотеки jsonrpcclient

## Тестирование

1. Запустите сервер
2. Используйте curl или Postman для отправки запросов
3. Проверьте ответы в формате JSON-RPC 2.0



Этот код — **минимальный JSON-RPC сервер** на базе `aiohttp` (асинхронный веб-сервер на Python) и `jsonrpcserver` (библиотека для обработки JSON-RPC 2.0 запросов). Он слушает POST-запросы на `/rpc` и выполняет зарегистрированные методы. Давай разберём **пошагово**:

---

### 🔧 Импорт библиотек

```python
from aiohttp import web
from jsonrpcserver import method, async_dispatch
```

* `aiohttp.web` — фреймворк для написания асинхронных HTTP-серверов.
* `jsonrpcserver.method` — декоратор для регистрации функций как методов JSON-RPC.
* `async_dispatch` — асинхронный обработчик JSON-RPC запросов.

---


### ✅ Преимущества такой схемы

* Полноценный JSON-RPC сервер за \~20 строк кода.
* Асинхронная обработка — можно обслуживать множество запросов параллельно.
* Расширяемость: легко добавлять новые методы.
* Поддержка спецификации JSON-RPC 2.0 (в отличие от "ручных" REST API).



curl.exe "http://localhost:5000/rpc?method=add&params[]=2&params[]=3&id=1"

curl.exe "http://localhost:5000/rpc?method=get_user&params[]=2&id=2"

