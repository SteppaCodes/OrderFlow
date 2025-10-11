from django.urls import path
from .views import OrderCreateAPIView

urlpatterns = [
    path('order/', OrderCreateAPIView.as_view(), name='order-create'),
]