# Чат на WebSocket и Redis

Это простой пример чата, использующий WebSocket для связи между клиентами и Redis Pub/Sub для распределения сообщений.

## Установка Redis

### Windows

1. Скачайте Redis для Windows с [GitHub](https://github.com/microsoftarchive/redis/releases)
2. Установите скачанный MSI-файл
3. Убедитесь, что Redis добавлен в PATH

### Linux

```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

### macOS

```bash
brew install redis
brew services start redis
```

## Проверка Redis

Запустите скрипт проверки Redis:

```bash
python redis_test.py
```

Если скрипт выдает ошибку, убедитесь, что Redis запущен:

- **Windows**: `redis-server` в командной строке
- **Linux**: `sudo systemctl start redis`
- **macOS**: `brew services start redis`

## Запуск чата

### С Redis (рекомендуется)

```bash
# Запуск с помощью скрипта (Windows)
run_with_redis.bat

# Или вручную
uvicorn main:app --reload
```

### Без Redis (ограниченный режим)

```bash
# Запуск с помощью скрипта (Windows)
run_without_redis.bat

# Или вручную
uvicorn main:app --reload
```

## Использование чата

1. Откройте в браузере: http://localhost:8000
2. Введите имя пользователя и нажмите "Подключиться"
3. Начните общение в чате

## Режимы работы

- **С Redis**: Полнофункциональный режим с поддержкой масштабирования
- **Без Redis**: Ограниченный режим, сообщения хранятся только в памяти сервера

## Структура проекта

- `main.py` - серверная часть на FastAPI с WebSocket
- `static/index.html` - клиентская часть с HTML, CSS и JavaScript
- `redis_test.py` - скрипт для проверки подключения к Redis
- `run_with_redis.bat` - скрипт для запуска с Redis (Windows)
- `run_without_redis.bat` - скрипт для запуска без Redis (Windows)