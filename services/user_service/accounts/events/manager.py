from typing import Optional
import json
from venv import logger
import pika
from threading import Lock
from django.conf import settings
import logging
import time

logger = logging.getLogger(__name__)

RABBITMQ_RETRY_ATTEMPTS = settings.RABBITMQ_RETRY_ATTEMPTS
RABBITMQ_RETRY_DELAY = settings.RABBITMQ_RETRY_DELAY

class RabbitMQConnectionManager:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # Initialize connection
        if self._initialized:
            return
            
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[pika.channel.Channel] = None
        self._initialized = True
        
        # Establish connection on initialization
        self._setup_connection()

    def _setup_connection(self):
        attempts = 0
        while attempts < RABBITMQ_RETRY_ATTEMPTS:
            try:
                credentials = pika.PlainCredentials(username=settings.RABBITMQ_USER,password=settings.RABBITMQ_PASSWORD)
                parameters = pika.ConnectionParameters(host=settings.RABBITMQ_HOST,port=settings.RABBITMQ_PORT,credentials=credentials,heartbeat=600,)
                
                self._connection = pika.BlockingConnection(parameters)
                self._channel = self._connection.channel()
                self._channel.confirm_delivery() 
                
                logger.info("RabbitMQConnectionManager: Connected and Channel opened.")
                return 

            except Exception as e:
                attempts += 1
                logger.error(f"RabbitMQ connection failed (attempt {attempts}/{RABBITMQ_RETRY_ATTEMPTS}): {e}")
                
                if attempts < RABBITMQ_RETRY_ATTEMPTS:
                    time.sleep(RABBITMQ_RETRY_DELAY)
                else:
                    logger.critical("Failed to establish connection to RabbitMQ after all attempts.")
                    raise ConnectionError("Could not establish connection to RabbitMQ") from e

    def _ensure_connection(self):
        # Check connection state
        if self._connection is None or self._connection.is_closed:
            logger.warning("Connection lost, attempting to reconnect...")
            self._setup_connection()
        
        # Check channel state (always runs if connection is open)
        if self._channel is None or self._channel.is_closed:
            logger.warning("Channel closed, creating new channel...")
            self._channel = self._connection.channel()
            self._channel.confirm_delivery()
            
    def get_channel(self) -> pika.channel.Channel:
        self._ensure_connection()
        return self._channel

    def publish_event(self, exchange, routing_key, message):
        try:
            channel = self.get_channel()
            
            # Declare exchange
            channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)
            
            # Publish message
            channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message), properties=pika.BasicProperties(delivery_mode=2,))
            
            logger.info(f"Successfully published event: {routing_key}")

        except pika.exceptions.NackError:
            logger.error(f"Broker rejected the message: {routing_key}")
            # You might want to implement retry logic here
        except pika.exceptions.UnroutableError:
            logger.error(f"Message was unroutable: {routing_key}")
        except Exception as e:
            logger.error(f"Error publishing event {routing_key}: {e}")
            self._connection = None 
            self._channel = None


_publisher = RabbitMQConnectionManager()