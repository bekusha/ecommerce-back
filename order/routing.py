from django.urls import path
from .consumers import OrderConsumer

websocket_urlpatterns = [
    path('ws/order/<int:user_id>/<str:device_id>/', OrderConsumer.as_asgi()),
]
