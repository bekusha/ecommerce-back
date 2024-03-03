from django.urls import path
from .views import store, paymentComplete, checkout

urlpatterns = [
    path('', store, name="store"),
    path('checkout/<int:pk>/', checkout, name="checkout"),
    path('complete/', paymentComplete, name="complete"),
]
