from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer
from .events.publisher import publish_order_placed

class OrderCreateAPIView(APIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        try:
            response = requests.get(f'http://127.0.0.1:8001/api/products/{product_id}/')
            if response.status_code != 200:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            
            product_response = response.json()
            product = product_response["data"]            
            quantity = serializer.validated_data["quantity"]

            # Check stock
            if product['stock'] < quantity:
                return Response({'error': 'Insufficient goods in stock'}, status=status.HTTP_400_BAD_REQUEST)

            total_price = float(product['price']) * quantity

            
            order = Order.objects.create(
                user_id=request.user.id,
                buyer_email = request.user.email,
                seller_email = product["seller_email"],
                product_id=product_id,
                product_name=product['name'],
                quantity=quantity,
                total_price=total_price
            )

            # Call Payment Service to create payment link
            try:
                payment_service_response = requests.post("http://127.0.0.1:8003/api/payment/create-link/")
                
                if payment_service_response.status_code != 201:
                    return Response({'error': 'Payment service error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
                payment_data = payment_service_response.json()
                payment_link = payment_data["data"]["link"]

            except requests.RequestException as e:
                return Response({'error': 'Could not connect to Payment Service'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            
            publish_order_placed(order, product)

            data = {
                "order": OrderSerializer(order).data,
                "payment_link": payment_link
            }
            
            return Response({"status":"success", "message":"Order placed successfully", "data":data}, status=status.HTTP_201_CREATED)
            
        except requests.RequestException as e:
            return Response({'error': f'Could not connect to Product Service: {e}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
