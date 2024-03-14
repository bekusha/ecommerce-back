from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import CartItem
from product.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True) 
    product = ProductSerializer(read_only=True) 

    class Meta:
        model = CartItem
        fields = ['id',  'quantity', 'product_id', 'product'] 
        
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
        cart = validated_data.pop('cart') 
        quantity = validated_data.get('quantity')
        
        # Create or update the cart item
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart, product=product,
            defaults={'quantity': quantity}
           
        )
        print(quantity)
        return cart_item
