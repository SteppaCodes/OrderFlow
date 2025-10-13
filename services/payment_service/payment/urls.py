from django.urls import path
from .views import PaymentLinkCreateAPIView, PaymentAPIView

urlpatterns = [
    path("payment/create-link/", PaymentLinkCreateAPIView.as_view(), name="create-link"),
    path("payment/", PaymentAPIView.as_view(), name="make-payment")
]