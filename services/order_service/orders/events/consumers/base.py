import queue
import pika
import json
from django.conf import settings
from .handlers import handle_payment_successful

def callback(ch, method, properties, body):
    message = json.loads(body)
    event = message.get("event")
    data = message.get("data")

    print(f"Received event: {event}")

    if event == "payment.successful":
        handle_payment_successful(data)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming():
    credentials = pika.PlainCredentials(username=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange="payment", exchange_type="topic", durable=True)

    result = channel.queue_declare(queue="order_service_queue", durable=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="payment", queue=queue_name, routing_key="payment.successful")

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print('Order Service: Waiting for messages...')
    channel.start_consuming()

