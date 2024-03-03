from rest_framework import serializers
from .models import CartItem
from product.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)  # Add this line

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_id']  # Include 'product_id'
        extra_kwargs = {'id': {'read_only': True}}

    def validate_quantity(self, value):
        """Ensure quantity is at least 1."""
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate_product_id(self, value):
        """Ensure the product exists."""
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("This product does not exist.")
        return value

    def create(self, validated_data):
        """Create or update the cart item with the given product and quantity."""
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        cart = validated_data.pop('cart')  # Assume cart is passed in context or validated_data
        quantity = validated_data.get('quantity')
        
        # Create or update the cart item
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
        )
        return cart_item
