from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

class ProductDetailAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = self.serializer_class(product)
            return Response({"status": "Success", "message": "Product retreived successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            return Response({"status": "Error", "message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ProductListCreateAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True)
        return Response({"status": "Success", "message": "Products retreived successfully", "data":serializer.data}, status=status.HTTP_200_OK)
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(seller_email=request.user.email)
        return Response({"status": "Success", "message": "Product created successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)

    def get_permission(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        return []
        