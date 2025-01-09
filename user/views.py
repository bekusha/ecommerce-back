
from rest_framework.permissions import IsAuthenticated
from server.settings import SIMPLE_JWT
from .serializers import  MileageRecordSerializer, UserRegistrationSerializer, UserDetailSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status
from rest_framework import permissions, status, views
from rest_framework.views import APIView
from .models import MileageRecord, User, Vendor
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
        

# class MileageRecordCreateView(CreateAPIView):
#     serializer_class = MileageRecordSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


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
    
@method_decorator(csrf_exempt, name='dispatch')
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

    def post (self, request, *args, **kwargs):
        
        response = super().post(request, *args, **kwargs)
        user = self.request.user

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response({
            'user':{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role':'CONSUMER'
            },
            'tokens': tokens
        })