from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from user.models import User
from django.core.exceptions import PermissionDenied



class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # if user.role != User.Role.CONSUMER:
        #     return Response({"error": "Only consumers can view the cart."}, status=403)
        
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        
        return Response(serializer.data)
    
class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        """ წაშლის ყველა CartItem-ს მომხმარებლის კალათიდან """
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        CartItem.objects.filter(cart=cart).delete()
        return Response({"message": "კალათა გასუფთავდა"}, status=status.HTTP_204_NO_CONTENT)

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        print("user role " + user.role)

            
        cart, _ = Cart.objects.get_or_create(user=user)
        serializer.save(cart=cart)

class UpdateCartItemView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class RemoveFromCartView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

