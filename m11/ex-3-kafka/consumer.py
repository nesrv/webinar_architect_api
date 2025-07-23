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

# Функция обработки заказа
def process_order(order):
    global processed_orders
    processed_orders += 1
    
    # Вывод информации о полученном заказе
    print(f"\n{Fore.BLUE}[↓] Получен заказ #{order['order_id']}{Style.RESET_ALL}")
    print(f"   Клиент: {Fore.CYAN}{order['customer']['name']}{Style.RESET_ALL}")
    print(f"   Статус: {Fore.YELLOW}{order['status']}{Style.RESET_ALL}")
    
    # Имитация обработки заказа с прогресс-баром
    processing_time = random.uniform(1, 3)  # Случайное время обработки
    print(f"   {Fore.WHITE}Обработка заказа: ", end="")
    
    steps = 20
    for i in range(steps + 1):
        progress = "█" * i + "░" * (steps - i)
        percent = i * 100 // steps
        print(f"\r   {Fore.WHITE}Обработка заказа: {Fore.GREEN}{progress} {percent}%{Style.RESET_ALL}", end="")
        time.sleep(processing_time / steps)
    
    print(f"\r   {Fore.GREEN}Обработка заказа: {'█' * steps} 100%{Style.RESET_ALL}")
    
    # Вывод итоговой информации
    print(f"   {Fore.GREEN}[✓] Заказ обработан успешно!{Style.RESET_ALL}")
    print(f"   Всего обработано заказов: {Fore.MAGENTA}{processed_orders}{Style.RESET_ALL}")
    print("-" * 50)

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
                # Конец партиции
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
    # Закрываем консьюмер
    consumer.close()