from django.urls import path
from .views import AboutPageView, ContactPageView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about_api'),
    path('contact/', ContactPageView.as_view(), name='contact_api'),
]