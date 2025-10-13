from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(write_only=True, required=True, max_length=16, min_length=13)
    cvv = serializers.CharField(write_only=True, required=True, max_length=4, min_length=3)
    expiry_date = serializers.CharField(write_only=True, required=True, max_length=5, min_length=5)

    class Meta:
        model = Payment
        fields = ['id', 'order_id', 'amount', 'status', 'created_at', 'card_number', 'cvv', 'expiry_date', 'order_id', 'amount']
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        validated_data.pop('card_number'), validated_data.pop('cvv'), validated_data.pop('expiry_date')

        payment = Payment.objects.create(**validated_data, status='successful')
        return payment