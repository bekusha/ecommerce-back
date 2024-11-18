from django.urls import path
from .views import PurchaseAPIView, OrderDetailsAPIView, OrderListAPIView
urlpatterns = [
    path('purchase/', PurchaseAPIView.as_view(), name='purchase'),
    path('', OrderListAPIView.as_view(), name='order_details'),
    path('<int:order_id>/', OrderDetailsAPIView.as_view(), name='order_details'),
]
