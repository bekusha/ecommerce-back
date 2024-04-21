from django.shortcuts import get_object_or_404
from rest_framework import generics

from user.models import User
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsVendorOrReadOnly
from rest_framework.permissions import IsAuthenticated

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
        # Get the category ID from the request data
        category_id = self.request.data.get('category', None)
        # If a category ID is provided, retrieve the category instance
        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id)
        # Save the product with the associated category
        serializer.save(vendor=self.request.user, category=category)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MyProductsAPIView(generics.ListAPIView):
    # serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view

    def get_queryset(self):
        """
        Returns a list of products for the currently authenticated vendor.
        """
        # user = self.request.user
        # if user.is_authenticated and user.role == User.Role.VENDOR:
        #     return Product.objects.filter(vendor=user)
        # else:
        #     return Product.objects.none() 
        
class ProductsByVendorAPIView(generics.ListAPIView):
    
    serializer_class = ProductSerializer

    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return Product.objects.filter(vendor_id=vendor_id)