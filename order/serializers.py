# create serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, SavedOrder

class OrderSerializer(serializers.ModelSerializer):
    oil_used_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_type', 'phone', 'address', 'email', 'ordered_at',
                  'status', 'courier_name', 'courier_phone', 'delivery_time',
                  'mileage', 'payment_status', 'user', 'oil_used_name']

    def get_oil_used_name(self, obj):
        # პირველი შეკვეთილი პროდუქტის პოვნა
        order_item = obj.order_items.first()
        if order_item and order_item.product:
            return order_item.product.name  # ვაბრუნებთ ზეთის სახელს
        return "უცნობი"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
class SavedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedOrder
        fields = '__all__'