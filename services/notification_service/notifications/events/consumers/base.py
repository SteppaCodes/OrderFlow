import pika
import json
from django.conf import settings
from .handlers import handle_order_confirmed

def callback(ch, method, properties, body):
    message = json.loads(body)
    event = message.get("event")
    data = message.get("data")

    print(f"Received event: {event}")

    if event == "order.confirmed":
        handle_order_confirmed(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming():
    credentials = pika.PlainCredentials(username=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange="payment", exchange_type="topic", durable=True)

    result = channel.queue_declare(queue="notification_service_queue", durable=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="orders", queue=queue_name, routing_key="order.*")

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print('Notification Service: Waiting for messages...')
    channel.start_consuming()

