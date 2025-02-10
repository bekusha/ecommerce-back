from django.urls import path, include


urlpatterns = [
    
    path('user/', include('user.urls')),
    path('product/',include('product.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('content/', include('content.urls')),
    path('ai/', include('ai.urls')),
    path('oils/', include('oils.urls')),
    path('changedelivery/', include('oilchangedelivery.urls'))
    
]

