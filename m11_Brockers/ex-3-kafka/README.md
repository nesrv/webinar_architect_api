# Визуализация работы Kafka

Этот проект демонстрирует работу брокера сообщений Kafka на примере системы обработки заказов.

## Компоненты системы

1. **Генератор заказов** (`producer.py`) - создает случайные заказы и отправляет их в топик Kafka
2. **Обработчик заказов** (`consumer.py`) - получает заказы из топика и обрабатывает их
3. **Монитор топика** (`monitor.py`) - отображает текущее состояние топика Kafka в реальном времени

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
python -m pip install -r requirements.txt
```

### 2. Запуск Kafka

Запустите Kafka с помощью Docker Compose:

```bash
docker compose up -d
```

Это запустит:
- Zookeeper (порт 2181)
- Kafka (порт 9092)
- Kafka UI (порт 8080) - веб-интерфейс для мониторинга Kafka

### 3. Запуск компонентов системы

#### Автоматический запуск всех компонентов:

**Windows:**
```bash
start_all.bat
```

**Linux/macOS:**
```bash
chmod +x *.sh
./start_all.sh
```

#### Ручной запуск каждого компонента:

**Windows:**
- Монитор: `start_monitor.bat`
- Обработчик: `start_consumer.bat`
- Генератор: `start_producer.bat`

**Linux/macOS:**
- Монитор: `./start_monitor.sh`
- Обработчик: `./start_consumer.sh`
- Генератор: `./start_producer.sh`

**Или напрямую через Python:**
```bash
python monitor.py    # Монитор
python consumer.py   # Обработчик
python producer.py   # Генератор
```

## Как это работает

1. **Генератор заказов** создает случайные заказы с разными товарами, ценами и данными клиентов и отправляет их в топик Kafka
2. **Обработчик заказов** получает заказы из топика Kafka и обрабатывает их с визуализацией прогресса
3. **Монитор топика** показывает текущее состояние топика, количество сообщений и скорость обработки

## Визуализация

- **Зеленый цвет** - успешные операции и сообщения, ожидающие обработки
- **Желтый цвет** - операции в процессе и сообщения в обработке
- **Синий цвет** - информационные сообщения
- **Красный цвет** - ошибки и предупреждения

## Управление

- Для остановки любого компонента нажмите **CTRL+C**
- Для просмотра Kafka UI откройте в браузере: http://localhost:8080

## Отличия от RabbitMQ

- Kafka использует модель публикации/подписки с сохранением сообщений
- Сообщения организованы в топики, которые разделены на партиции
- Kafka хранит сообщения в течение настраиваемого времени, даже после их обработки
- Поддерживает горизонтальное масштабирование через партиции и группы потребителей