from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import OilChangeDelivery
from .serializers import OilChangeDeliverySerializer

# List and create OilChangeDeliveries
class OilChangeDeliveryListCreate(ListCreateAPIView):
    queryset = OilChangeDelivery.objects.all()
    serializer_class = OilChangeDeliverySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assign the request user to the user field
        serializer.save(user=self.request.user)

# Retrieve, update, and delete specific OilChangeDelivery
class OilChangeDeliveryDetail(RetrieveUpdateDestroyAPIView):
    queryset = OilChangeDelivery.objects.all()
    serializer_class = OilChangeDeliverySerializer
    permission_classes = [IsAuthenticated]

# List OilChangeDeliveries specific to the authenticated user
class UserOilChangeDeliveryListView(ListAPIView):
    serializer_class = OilChangeDeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter to only include deliveries associated with the authenticated user
        return OilChangeDelivery.objects.filter(user=self.request.user)
