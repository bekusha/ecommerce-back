
from .serializers import  MileageRecordSerializer,  UserDetailSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from rest_framework import permissions, status, views
from rest_framework.views import APIView
from .models import MileageRecord, User, Vendor
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class CheckOrCreateConsumerView(APIView):
    """
    API View for creating or checking a Consumer user based on the provided device_id.
    """
    def post(self, request, *args, **kwargs):
        device_id = request.data.get('device_id', None)
        if not device_id:
            return Response({'error': 'device_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check or create user
        user, created = User.objects.get_or_create(
            device_id=device_id,
            defaults={
                'username': f"user_{device_id}",
                'role': 'CONSUMER',
            }
        )
        
        if created:
            user.set_password(User.objects.make_random_password())
            user.save()
            return Response({'message': 'Consumer created successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)

        return Response({'message': 'Consumer already exists', 'user_id': user.id}, status=status.HTTP_200_OK)



class UserDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # The request.user property will have the user instance for authenticated requests
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

class VendorDetailView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = UserDetailSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        

class MileageRecordCreateView(CreateAPIView):
    serializer_class = MileageRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Delete existing mileage records before saving the new one
        MileageRecord.objects.filter(user=self.request.user).delete()
        # Save the new mileage record
        serializer.save(user=self.request.user)

class MileageRecordListView(ListAPIView):
    queryset = MileageRecord.objects.all()
    serializer_class = MileageRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return records only for the authenticated user
        return self.queryset.filter(user=self.request.user)
    
