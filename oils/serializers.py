from rest_framework import serializers
from .models import HomeOilDeliveryRequest

class HomeOilDeliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeOilDeliveryRequest
        fields = '__all__'
