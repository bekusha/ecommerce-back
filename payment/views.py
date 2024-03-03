from django.shortcuts import render
from product.models import Product
import json
from django.http import JsonResponse
from rest_framework import generics
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


def checkout(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, 'base/checkout.html', context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'base/store.html', context)

def paymentComplete(request):
    body = json.loads(request.body)
    print('Body: ', body)
    return JsonResponse('Payment completed!', safe=False)




# class OrderListCreate(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# class OrderItemListCreate(generics.ListCreateAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

# class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
