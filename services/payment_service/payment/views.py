import re
from rest_framework.views import APIView
from .serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework import status
from .events.publisher import publish_payment_successful


class PaymentLinkCreateAPIView(APIView):

    def post(self, request):
        return Response({"message": "Payment link created successfully", "data":{"link": "http//:linktopayment.com"}}, status=status.HTTP_201_CREATED)

class PaymentAPIView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        publish_payment_successful(serializer.data)

        return Response({"message": "Payment made successfully", "data": serializer.data}, status=status.HTTP_200_OK)



