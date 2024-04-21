# transactions/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction, TransactionItem, User
from .serializers import TransactionSerializer
from django.db import transaction as db_transaction

@api_view(['POST'])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        with db_transaction.atomic():
            transaction = serializer.save()  # Save the transaction
            # Assume we save transaction items separately or they're included in the serializer
            payout_results = []
            for item in transaction.items.all():
                payout_result = create_payout(item.product.vendor.paypal_address, item.product.price * item.quantity)
                payout_results.append(payout_result)
            return Response({
                "transaction": serializer.data,
                "payouts": payout_results
            }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_payout(paypal_address, amount):
    # Here you would integrate with PayPal's Payout API
    # This is a placeholder function to illustrate the flow
    return {"address": paypal_address, "amount": amount, "status": "Success"}
