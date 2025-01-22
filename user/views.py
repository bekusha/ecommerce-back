
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


User = get_user_model()

class CheckOrCreateConsumerView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        # მიიღე `device_id` პარამეტრიდან ან `headers`-დან
        device_id = kwargs.get('device_id') or request.headers.get('Device-ID')

        if not device_id:
            return Response({'error': 'Device ID is required.'}, status=400)

        # მოძებნე მომხმარებელი
        user, created = User.objects.get_or_create(
            device_id=device_id,
            defaults={
                'username': f"user_{device_id}",
                'role': User.Role.CONSUMER,
                'password': User.objects.make_random_password(),
            }
        )

        # თუ მომხმარებელი უკვე არსებობს, დავამატოთ აკლებული ველები
        if not created:
            updated = False
            if not user.username.startswith("user_"):
                user.username = f"user_{device_id}"
                updated = True
            if user.role != User.Role.CONSUMER:
                user.role = User.Role.CONSUMER
                updated = True
            if not user.password:  # თუ მომხმარებელს არ აქვს პაროლი
                user.set_password(User.objects.make_random_password())
                updated = True

            if updated:
                user.save()  # შევინახოთ ცვლილებები

        # დავაბრუნოთ მომხმარებლის დეტალები
        serializer = UserDetailSerializer(user)
        return Response(
            {
                'message': 'Consumer created successfully' if created else 'Consumer updated successfully',
                'user': serializer.data,
            },
            status=201 if created else 200
        )






# class CheckOrCreateConsumerView(APIView):
#     """
#     API View for creating or checking a Consumer user based on the provided device_id.
#     """
#     def post(self, request, *args, **kwargs):
#         device_id = request.data.get('device_id', None)
#         if not device_id:
#             return Response({'error': 'device_id is required'}, status=status.HTTP_400_BAD_REQUEST)

#         # Check or create user
#         user, created = User.objects.get_or_create(
#             device_id=device_id,
#             role='CONSUMER',
#             defaults={
#                 'username': f"user_{device_id}",
#                 'role': 'CONSUMER',
#             }
#         )

#         if created:
#             user.set_password(User.objects.make_random_password())
#             user.save()

#         # Serialize the user instance
#         serializer = UserDetailSerializer(user)

#         # Return full user details
#         return Response(
#             {
#                 'message': 'Consumer created successfully' if created else 'Consumer already exists',
#                 'user': serializer.data  # This ensures full user details are included
#             },
#             status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
#         )




class UserDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     # The request.user property will have the user instance for authenticated requests
    #     user = request.user
    #     serializer = UserDetailSerializer(user)
    #     return Response(serializer.data)

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
    
