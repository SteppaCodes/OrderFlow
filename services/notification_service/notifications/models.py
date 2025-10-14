from django.db import models
import uuid

class Notification(models.Model):
    TYPE_CHOICES = [
        ('order_confirmed', 'Order Placed'),
        ('payment_successful', 'Payment Successful'),
        ('stock_updated', 'Stock Updated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    recipient = models.CharField(max_length=200) 
    message = models.TextField()
    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.type} - {self.recipient}"