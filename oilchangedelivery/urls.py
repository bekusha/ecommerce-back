from django.urls import path
from .views import (

    OilChangeDeliveryListCreate,
    OilChangeDeliveryDetail,
    UserOilChangeDeliveryListView,  # დამატებულია მომხმარებლის სპეციფიკური ვიუ
)

urlpatterns = [
    path('', OilChangeDeliveryListCreate.as_view(), name='oilchangedelivery-list-create'),
    path('<int:pk>/', OilChangeDeliveryDetail.as_view(), name='oilchangedelivery-detail'),  # დავამატე '/' ბოლოში, რათა URL იყოს სწორი ფორმატით

    path('user-orders/', UserOilChangeDeliveryListView.as_view(), name='user-oilchangedelivery-list'),  # მომხმარებლის ჩანაწერების ნახვა
]
