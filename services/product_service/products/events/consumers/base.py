from django.conf import settings
import pika
import json
from .handlers import handle_order_placed, handle_order_confirmed


def callback(ch, method, properties, body):
    message = json.loads(body)
    event = message.get('event')
    data = message.get('data')
    
    print(f"Received event: {event}")
    
    if event == 'order.placed':
        handle_order_placed(data)
    elif event == 'order.confirmed':
        handle_order_confirmed(data)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consuming():
    credentials = pika.PlainCredentials(username=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=settings.RABBITMQ_HOST,port=settings.RABBITMQ_PORT,credentials=credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    # Declare exchange
    channel.exchange_declare(exchange='orders', exchange_type='topic', durable=True)

    # Declare and bind queue
    result = channel.queue_declare(queue='product_service_queue', durable=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='orders', queue=queue_name, routing_key='order.*')
    
    # Start consuming
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    
    print('Product Service: Waiting for messages...')
    channel.start_consuming()
