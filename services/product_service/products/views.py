from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductDetailAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = self.serializer_class(product)
            return Response({"status": "Success", "message": "Product retreived successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response({"status": "Error", "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ProductListAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True)
        return Response({"status": "Success", "message": "Products retreived successfully", "data":serializer.data}, status=status.HTTP_200_OK)