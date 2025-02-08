from django.urls import path
from . import views

urlpatterns = [
    path('detail/', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:pk>/', views.UpdateCartItemView.as_view(), name='update_cart_item'), 
    path('remove/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
     path('cart/clear/', views.ClearCartView.as_view(), name='clear-cart'),
]
