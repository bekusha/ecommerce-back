
from rest_framework.permissions import IsAuthenticated
from server.settings import SIMPLE_JWT
from .serializers import  UserRegistrationSerializer, UserDetailSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from rest_framework import permissions, status, views
from rest_framework.views import APIView
from .models import User, Vendor


from django.http import JsonResponse

class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        

class UpdatePayPalAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Retrieve the PayPal address from the request data
        paypal_address = request.data.get('paypal_address')

        # Update the user's PayPal address (assuming you have a custom User model)
        request.user.paypal_address = paypal_address
        request.user.save()

        # Optionally, return a response confirming the address was updated
        return Response({'message': 'PayPal address updated successfully'}, status=200)
    
class FetchPayPalAddressView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = User.objects.get(id=vendor_id, role=User.Role.VENDOR)
            # Assuming PayPal address is stored in the 'paypal_address' field of the User model
            paypal_address = vendor.paypal_address
            return Response({'paypal_address': paypal_address}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        
