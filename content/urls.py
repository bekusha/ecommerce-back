from django.urls import path
from .views import AboutPageView, ContactPageView, MainPageListView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about_api'),
    path('contact/', ContactPageView.as_view(), name='contact_api'),
    path('main/', MainPageListView.as_view(), name='main_api'),
]