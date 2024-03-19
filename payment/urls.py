from django.urls import path
from .views import create_transaction, RetrieveTransactionView

urlpatterns = [
    path('transactions/', create_transaction, name='transactions'),
     path('transactions/<str:transaction_id>/', RetrieveTransactionView.as_view(), name='retrieve-transaction'),
    
]
