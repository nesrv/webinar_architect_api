import pika
import json
import time
import random
import colorama
from colorama import Fore, Style

# Инициализация colorama для цветного вывода
colorama.init()

# Счетчик обработанных заказов
processed_orders = 0

# Функция обработки заказа
def callback(ch, method, properties, body):
    global processed_orders
    order = json.loads(body)
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
    
    # Подтверждение обработки
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Настройка очереди
channel.queue_declare(queue='orders', durable=True)
channel.basic_qos(prefetch_count=1)  # Обрабатывать по 1 сообщению за раз

# Подписка на очередь
channel.basic_consume(queue='orders', on_message_callback=callback)

print(f"{Fore.BLUE}[*] Обработчик заказов запущен. Для выхода нажмите CTRL+C{Style.RESET_ALL}")
print("-" * 50)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\n{Fore.RED}[!] Обработчик заказов остановлен{Style.RESET_ALL}")
    connection.close()