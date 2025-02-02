# create serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, SavedOrder

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
class SavedOrderSerializer(serializers.ModelSerializer):
    oil_used_name = serializers.CharField(source="oil_used.name", read_only=True)  # იღებს ზეთის სახელს

    class Meta:
        model = SavedOrder
        fields = ['id', 'oil_used_name', 'mileage', 'oil_used', 'created_at']