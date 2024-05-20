from django.urls import path
from .views import OilRecommendationAPIView

urlpatterns = [
    path('oil/', OilRecommendationAPIView.as_view(), name='get-oil-recommendation'),
]
