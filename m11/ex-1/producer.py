import pika
import json

# Подключение
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди
channel.queue_declare(queue='orders', durable=True)  # durable - сохраняет очередь при перезапуске

# Отправка сообщения
message = {
    "order_id": 123,
    "status": "new",
    "items": ["book", "pen"]
}
channel.basic_publish(
    exchange='',
    routing_key='orders',
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=2  # Сохранять сообщения на диске
    )
)

print(" [x] Отправлено сообщение")
connection.close()