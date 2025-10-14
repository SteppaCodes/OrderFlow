from django.urls import path
from .views import ProductDetailAPIView, ProductListCreateAPIView

urlpatterns = [
    path('products/<uuid:product_id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list'),
]