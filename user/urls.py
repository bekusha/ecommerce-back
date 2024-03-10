from django.urls import path
from .views import UserRegistrationAPIView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Updated to use custom view
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Updated to use custom view
    path('detail/', UserDetailView.as_view(), name = 'user-details')
]
