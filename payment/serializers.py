from rest_framework import serializers
from .models import Transaction, TransactionItem, Product
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = TransactionItem
        fields = ['product', 'quantity', 'price_at_transaction']

class TransactionSerializer(serializers.ModelSerializer):
    items = TransactionItemSerializer(many=True, write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = ['user', 'transaction_id', 'total_amount', 'currency', 'created_at', 'updated_at', 'payer_details', 'items']
        read_only_fields = ['created_at', 'updated_at']

    # def create(self, validated_data):
    #     items_data = validated_data.pop('items')
    #     # Manually set the user from the request context
    #     validated_data['user'] = self.context['request'].user
    #     transaction = Transaction.objects.create(**validated_data)
    #     for item_data in items_data:
    #         TransactionItem.objects.create(**item_data, transaction=transaction)
    #     return transaction

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        transaction = Transaction.objects.create(**validated_data)
        for item_data in items_data:
            product = Product.objects.get(pk=item_data['product'].id)
            TransactionItem.objects.create(
                transaction=transaction,
                product=product,
                quantity=item_data['quantity'],
                price_at_transaction=product.price  # This ensures the correct, latest price is used
            )
        return transaction
