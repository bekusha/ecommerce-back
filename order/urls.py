from django.urls import path
from .views import PurchaseAPIView, OrderDetailsAPIView, OrderListAPIView, SavedOrderListAPIView
urlpatterns = [
    path('purchase/', PurchaseAPIView.as_view(), name='purchase'),
    path('', OrderListAPIView.as_view(), name='order_details'),
    path('<int:order_id>/', OrderDetailsAPIView.as_view(), name='order_details'),
    path('saved-orders/', SavedOrderListAPIView.as_view(), name='saved_orders'),
]
