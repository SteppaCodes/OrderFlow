from django.core.management.base import BaseCommand
from ...events.consumers.base import start_consuming

class Command(BaseCommand):
    help = "Start RabbitMQ consumer for events"

    def handle(self, *args, **kwargs):
        start_consuming()