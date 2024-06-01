from rest_framework import generics, serializers
from .models import HomeOilDeliveryRequest
from .serializers import HomeOilDeliveryRequestSerializer

class HomeOilDeliveryRequestCreateView(generics.CreateAPIView):
    queryset = HomeOilDeliveryRequest.objects.all()
    serializer_class = HomeOilDeliveryRequestSerializer

    def perform_create(self, serializer):
        product = self.request.data.get('product')
        product_name = self.request.data.get('product_name')

        if product:
            serializer.save(product_id=product)
        elif product_name:
            serializer.save(product_name=product_name)
        else:
            raise serializers.ValidationError("You must provide either a product or a product name.")
