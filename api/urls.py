from django.urls import path, include
from rest_framework.routers import DefaultRouter

# The API URLs are now determined automatically by the router.
urlpatterns = [
    
    path('user/', include('user.urls')),
]