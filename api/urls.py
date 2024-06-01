from django.urls import path, include



urlpatterns = [
    
    path('user/', include('user.urls')),
    path('product/',include('product.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('content/', include('content.urls')),
    path('ai/', include('ai.urls')),
    path('oils/', include('oils.urls'))
    
    
]