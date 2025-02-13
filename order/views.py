from django.shortcuts import get_object_or_404
from order.serializers import OrderItemSerializer, OrderSerializer, SavedOrderSerializer
import logging

logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions

from order.models import Order, OrderItem, SavedOrder  # Order, OrderItem და SavedOrder მოდელებიდან
from product.models import Product  # Product მოდელიდან'
from django.db import transaction

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
# @transaction.atomic
class PurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_items = request.data.get('order_items', [])
        order_type = request.data.get('order_type', 'product_delivery')  
        phone = request.data.get('phone')
        address = request.data.get('address')
        email = request.data.get('email')
        logger.error(f"Received request data: {request.data}") 
        print("order items" , order_items)
        
        if not order_items:
            logger.error("❌ order_items ცარიელია")
            return Response({"error": "order_items ცარიელია"}, status=status.HTTP_400_BAD_REQUEST)


        # გადაამოწმე სწორი ტიპი
        if order_type not in dict(Order.ORDER_TYPE_CHOICES):
            return Response({"detail": "Invalid order type."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new order
        order = Order.objects.create(user=user,
                                    order_type=order_type,
                                    phone=phone,
                                    address=address,
                                    email=email
                                     )

        for item in order_items:
            logger.error(f"Processing item: {item}")
            if not isinstance(item, dict):
                return Response({"error": "Order item უნდა იყოს ობიექტის ტიპის"}, status=status.HTTP_400_BAD_REQUEST)

            product_id = item.get("product_id") or item.get("id")  # ეძებს product_id-ს, თუ არაა, მაშინ id-ს იღებს

            if not product_id:
                return Response({"error": "order_items-ს აკლია product_id ან id"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                print("product_id", product_id)
                product = get_object_or_404(Product, id=product_id)
            except Exception as e:
                logger.error(f"Product not found: {e}")
                return Response({"error": f"პროდუქტი id={product_id} ვერ მოიძებნა"}, status=status.HTTP_400_BAD_REQUEST)
            print("item", item)
            quantity = item.get("quantity")

            if quantity > product.quantity:
                return Response({"detail": f"{product.name} მარაგში არ არის საკმარისი."}, status=status.HTTP_400_BAD_REQUEST)

            # Create an OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

            # Reduce product stock
            product.quantity -= quantity
            product.save()


        return Response({"message": "შეკვეთა წარმატებით გაფორმდა!", "order_id": order.id}, status=status.HTTP_201_CREATED)
    

# class SavedOrderViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API ViewSet for SavedOrders
#     """
#     queryset = SavedOrder.objects.all()
#     serializer_class = SavedOrderSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def __init__(self, *args, **kwargs):
#         print(f"Initializing SavedOrderViewSet with args: {args}, kwargs: {kwargs}")
#         super().__init__(*args, **kwargs)

class SavedOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved_orders = SavedOrder.objects.filter(user=request.user)
        serializer = SavedOrderSerializer(saved_orders, many=True)
        return Response(serializer.data) 
