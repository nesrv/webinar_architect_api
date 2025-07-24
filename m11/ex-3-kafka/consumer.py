import json
import time
import random
import colorama
from colorama import Fore, Style
from confluent_kafka import Consumer, KafkaError

# Инициализация colorama для цветного вывода
colorama.init()

# Настройки Kafka
KAFKA_TOPIC = 'orders'
KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order-processing-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

# Счетчик обработанных заказов
processed_orders = 0

# Функция для генерации цвета по ID заказа
def get_order_color(order_id):
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    return colors[order_id % len(colors)]

# Функция обработки заказа
def process_order(order):
    global processed_orders
    processed_orders += 1
    
    order_color = get_order_color(order['order_id'])
    
    # Вывод информации о полученном заказе
    print(f"\n{order_color}{'='*20} CONSUMER {'='*20}{Style.RESET_ALL}")
    print(f"{order_color}[↓] ПОЛУЧЕН ЗАКАЗ #{order['order_id']}{Style.RESET_ALL}")
    print(f"{order_color}Клиент: {order['customer']['name']}{Style.RESET_ALL}")
    print(f"{order_color}Статус: {order['status']}{Style.RESET_ALL}")
    print(f"{order_color}Итого: {order['total']} ₽{Style.RESET_ALL}")
    
    # Имитация обработки заказа с прогресс-баром
    processing_time = random.uniform(2, 4)
    print(f"{order_color}Обработка: ", end="")
    
    steps = 15
    for i in range(steps + 1):
        progress = "█" * i + "░" * (steps - i)
        percent = i * 100 // steps
        print(f"\r{order_color}Обработка: {progress} {percent}%{Style.RESET_ALL}", end="")
        time.sleep(processing_time / steps)
    
    print(f"\r{order_color}Обработка: {'█' * steps} 100%{Style.RESET_ALL}")
    
    # Вывод итоговой информации
    print(f"{order_color}[✓] ЗАКАЗ ОБРАБОТАН!{Style.RESET_ALL}")
    print(f"{order_color}Всего: {processed_orders}{Style.RESET_ALL}")
    print(f"{order_color}{'='*50}{Style.RESET_ALL}")
    time.sleep(1)

# Создание консьюмера Kafka
consumer = Consumer(KAFKA_CONFIG)

# Подписка на топик
consumer.subscribe([KAFKA_TOPIC])

print(f"{Fore.BLUE}[*] Обработчик заказов Kafka запущен. Для выхода нажмите CTRL+C{Style.RESET_ALL}")
print(f"{Fore.BLUE}[*] Подключение к Kafka: {KAFKA_CONFIG['bootstrap.servers']}, топик: {KAFKA_TOPIC}{Style.RESET_ALL}")
print("-" * 50)

# Основной цикл получения и обработки сообщений
try:
    while True:
        # Получаем сообщение с таймаутом 1 секунда
        msg = consumer.poll(1.0)
        
        if msg is None:
            continue
        
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"{Fore.YELLOW}[!] Достигнут конец партиции{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Ошибка: {msg.error()}{Style.RESET_ALL}")
        else:
            # Парсим сообщение
            try:
                order = json.loads(msg.value().decode('utf-8'))
                process_order(order)
                # Подтверждаем обработку сообщения
                consumer.commit(msg)
            except json.JSONDecodeError as e:
                print(f"{Fore.RED}[!] Ошибка парсинга JSON: {e}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Ошибка обработки: {e}{Style.RESET_ALL}")

except KeyboardInterrupt:
    print(f"\n{Fore.RED}[!] Обработчик заказов остановлен{Style.RESET_ALL}")
finally:
    consumer.close()