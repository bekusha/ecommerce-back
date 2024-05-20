from rest_framework import serializers

class CarQuerySerializer(serializers.Serializer):
    car_model_year = serializers.CharField(required=True, max_length=100)
