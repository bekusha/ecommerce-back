from django.urls import path
from .views import PaymentCallbackApiView, PurchaseAPIView, OrderDetailsAPIView, OrderListAPIView, SavedOrderListAPIView, redirect_after_payment
urlpatterns = [
    path('purchase/', PurchaseAPIView.as_view(), name='purchase'),
    path('', OrderListAPIView.as_view(), name='order_details'),
    path('<int:order_id>/', OrderDetailsAPIView.as_view(), name='order_details'),
    path('saved-orders/', SavedOrderListAPIView.as_view(), name='saved_orders'),
    path('callback/', PaymentCallbackApiView.as_view(), name='payment-callback'),
    path('redirect/<int:order_id>/', redirect_after_payment, name='payment_redirect'),
    # path("order/payment-callback/", PaymentCallbackApiView.as_view(), name="payment-callback"),
]
