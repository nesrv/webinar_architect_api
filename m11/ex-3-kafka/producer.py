import json
import time
import random
import datetime
from faker import Faker
import colorama
from colorama import Fore, Style
from confluent_kafka import Producer

# Инициализация colorama для цветного вывода
colorama.init()

# Инициализация Faker для генерации случайных данных
fake = Faker('ru_RU')

# Настройки Kafka
KAFKA_TOPIC = 'orders'
KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'order-producer'
}

# Создание продюсера Kafka
producer = Producer(KAFKA_CONFIG)

# Функция для обработки результата отправки сообщения
def delivery_report(err, msg):
    if err is not None:
        print(f"{Fore.RED}[!] Ошибка отправки сообщения: {err}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}[✓] Сообщение отправлено в топик {msg.topic()} [{msg.partition()}] @ {msg.offset()}{Style.RESET_ALL}")

# Список возможных товаров
products = [
    "Смартфон", "Ноутбук", "Наушники", "Клавиатура", "Мышь", "Монитор", 
    "Планшет", "Умные часы", "Колонка", "Зарядное устройство", "Чехол",
    "Кабель", "Флешка", "Внешний диск", "Веб-камера"
]

# Статусы заказов
statuses = ["новый", "оплачен", "в обработке", "отправлен"]

# Функция для генерации случайного заказа
def generate_order():
    order_id = random.randint(10000, 99999)
    items_count = random.randint(1, 5)
    items = random.sample(products, items_count)
    prices = [random.randint(500, 15000) for _ in range(items_count)]
    
    return {
        "order_id": order_id,
        "customer": {
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number()
        },
        "status": random.choice(statuses),
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": [{
            "name": items[i],
            "price": prices[i],
            "quantity": random.randint(1, 3)
        } for i in range(items_count)],
        "total": sum(prices)
    }

# Функция для отправки заказа в топик Kafka
def send_order(order):
    # Преобразуем заказ в JSON
    order_json = json.dumps(order, ensure_ascii=False).encode('utf-8')
    
    # Отправляем сообщение в Kafka
    producer.produce(
        KAFKA_TOPIC,
        key=str(order['order_id']),
        value=order_json,
        callback=delivery_report
    )
    
    # Обрабатываем все ожидающие сообщения
    producer.poll(0)
    
    # Красивый вывод информации о заказе
    print(f"{Fore.GREEN}[✓] Отправлен заказ #{order['order_id']}{Style.RESET_ALL}")
    print(f"   Клиент: {Fore.CYAN}{order['customer']['name']}{Style.RESET_ALL}")
    print(f"   Статус: {Fore.YELLOW}{order['status']}{Style.RESET_ALL}")
    print(f"   Товары ({len(order['items'])}):")    
    for item in order['items']:
        print(f"     - {item['name']} x{item['quantity']} = {Fore.MAGENTA}{item['price'] * item['quantity']} ₽{Style.RESET_ALL}")
    print(f"   {Fore.WHITE}Итого: {Fore.MAGENTA}{order['total']} ₽{Style.RESET_ALL}")
    print(f"   Время: {order['created_at']}")
    print("-" * 50)

# Основной цикл генерации заказов
try:
    print(f"{Fore.BLUE}[*] Генератор заказов Kafka запущен. Для остановки нажмите CTRL+C{Style.RESET_ALL}")
    print(f"{Fore.BLUE}[*] Подключение к Kafka: {KAFKA_CONFIG['bootstrap.servers']}, топик: {KAFKA_TOPIC}{Style.RESET_ALL}")
    print("-" * 50)
    
    while True:
        order = generate_order()
        send_order(order)
        # Случайная пауза между заказами (от 1 до 5 секунд)
        delay = random.uniform(1, 5)
        time.sleep(delay)
        
except KeyboardInterrupt:
    print(f"\n{Fore.RED}[!] Генератор заказов остановлен{Style.RESET_ALL}")
    # Отправляем все оставшиеся сообщения перед завершением
    producer.flush()