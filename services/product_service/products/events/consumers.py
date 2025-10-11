from django.conf import settings
import pika
import json
import os
from products.models import Product
from .publishers import publish_stock_updated, publish_stock_reserved
from django.db import transaction

def callback(ch, method, properties, body):
    message = json.loads(body)
    event = message.get('event')
    data = message.get('data')
    
    print(f"Received event: {event}")
    
    if event == 'order.placed':
        handle_order_placed(data)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def handle_order_placed(data):
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    order_id = data.get('order_id')
    
    try:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=product_id)

            if product.stock >= quantity:
                product.stock -= quantity
                product.reserved_stock = product.reserved_stock + quantity
                product.save()

                publish_stock_reserved(product, str(order_id))
                print(f"Reserved {quantity} of product {product_id} for order {order_id}")
            else:
                print(f"Insufficient stock for product {product_id}")
    except Product.DoesNotExist:
        print(f"Product {product_id} not found")
    except Exception as e:
        print(f"Error reserving stock for order {order_id}: {e}")



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
    channel.queue_bind(exchange='orders', queue=queue_name, routing_key='order.placed')
    
    # Start consuming
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    
    print('Product Service: Waiting for messages...')
    channel.start_consuming()
