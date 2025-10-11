from django.core.management.base import BaseCommand
from ...events.consumers import start_consuming

class Command(BaseCommand):
    help = "Start RabbitMQ consumer for order.placed events"

    def handle(self, *args, **kwargs):
        start_consuming()