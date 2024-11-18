from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OilChangeDelivery

User = get_user_model()

class OilChangeDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = OilChangeDelivery
        fields = ['id', 'user', 'phone', 'address', 'email',  'ordered_at', 'status', 'car_make_model_year', 'product']
        read_only_fields = ['user']  # Mark user field as read-only to prevent client from setting it

    def create(self, validated_data):
        # Automatically assign the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
