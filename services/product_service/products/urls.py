from django.urls import path
from .views import ProductDetailAPIView, ProductListAPIView

urlpatterns = [
    path('products/<uuid:product_id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
]