from django.urls import path
from .views import HomeOilDeliveryRequestCreateView

urlpatterns = [
    path('oil-delivery-requests/', HomeOilDeliveryRequestCreateView.as_view(), name='oil-delivery-request-create'),
]
