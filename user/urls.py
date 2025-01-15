from django.urls import path


from .views import CheckOrCreateConsumerView,  MileageRecordListView,   UserDetailView, VendorDetailView,  MileageRecordCreateView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('register/', UserRegistrationAPIView.as_view(), name='register'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Updated to use custom view
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Updated to use custom view
    path('detail/', UserDetailView.as_view(), name = 'user-details'),
    path('vendor/<int:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),
    # path('update-paypal-address/', UpdatePayPalAddressView.as_view(), name='update_paypal_address'),
    # path('vendor/paypal-address/<int:vendor_id>/', FetchPayPalAddressView.as_view(), name='fetch_paypal_address'),
    path('mileage/create/', MileageRecordCreateView.as_view(), name='mileage_create'), 
    path('mileage/list/', MileageRecordListView.as_view(), name='mileage_list'),  
    path('create-consumer/', CheckOrCreateConsumerView.as_view(), name='create_consumer'),
    # path('facebooklogin/', FacebookLogin.as_view(), name='facebooklogin'),
]
 