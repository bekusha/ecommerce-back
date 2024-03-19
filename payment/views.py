from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TransactionSerializer
from rest_framework.generics import RetrieveAPIView
from .models import Transaction
from .serializers import TransactionSerializer

@api_view(['POST'])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveTransactionView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'transaction_id'