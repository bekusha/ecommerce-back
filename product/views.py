from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsVendorOrReadOnly

class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the products
        for the currently authenticated user filtered by category if provided.
        """
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
