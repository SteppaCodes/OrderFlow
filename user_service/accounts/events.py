import pika
import json
from django.conf import settings

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(username=settings.RABBITMQ_USER, password=settings.RABBITMQ_PASSWORD
    )
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

def publish_event(exchange, routing_key, message):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
        
        # Publish message
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        
        connection.close()
        print(f"Published event: {routing_key}")
    except Exception as e:
        print(f"Error publishing event: {e}")


def publish_user_created(user):
    message = {
        'event': 'user.created',
        'data': {
            'user_id': str(user.id),
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
    }

    publish_event('users', 'user.created', message)