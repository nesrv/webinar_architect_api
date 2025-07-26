import pika
import json
import time

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f" [x] Обработка заказа {order['order_id']}")
    time.sleep(2)  # Имитация обработки
    print(" [x] Готово")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Подтверждение обработки

# Подключение
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Настройка очереди
channel.queue_declare(queue='orders', durable=True)
channel.basic_qos(prefetch_count=1)  # Обрабатывать по 1 сообщению за раз

# Подписка
channel.basic_consume(queue='orders', on_message_callback=callback)

print(' [*] Ожидание сообщений. Для выхода нажмите CTRL+C')
channel.start_consuming()