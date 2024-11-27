from django.shortcuts import get_object_or_404
from order.serializers import OrderItemSerializer, OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from order.models import Order, OrderItem  # Order და OrderItem მოდელებიდან
from product.models import Product  # Product მოდელიდან'

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# get order details
class OrderDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order_serializer = OrderSerializer(order)
        order_items = OrderItem.objects.filter(order=order)
        order_items_serializer = OrderItemSerializer(order_items, many=True)

        return Response({
            'order': order_serializer.data,
            'order_items': order_items_serializer.data
        }, status=status.HTTP_200_OK)


# Create your views here.
class PurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_items = request.data.get('order_items', [])
        order_type = request.data.get('order_type', 'product_delivery')  
        phone = request.data.get('phone')
        address = request.data.get('address')
        email = request.data.get('email')
        
        # Check for valid order type
        if order_type not in dict(Order.ORDER_TYPE_CHOICES):
            return Response({"detail": "Invalid order type."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new order
        order = Order.objects.create(
            user=user,
            order_type=order_type,
            phone=phone,
            address=address,
            email=email
        )

        for item in order_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)  # Default quantity to 1

            product = None
            if product_id:
                product = Product.objects.filter(id=product_id).first()
                if not product:
                    return Response({"detail": f"Product with ID {product_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
                if quantity > product.quantity:
                    return Response({"detail": f"{product.name} is out of stock."}, status=status.HTTP_400_BAD_REQUEST)

                # Reduce product stock
                product.quantity -= quantity
                product.save()

            # Create an OrderItem (product can be None)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        return Response({"message": "Order successfully created!", "order_id": order.id}, status=status.HTTP_201_CREATED)
