from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsVendorOrReadOnly  

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly]  

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsVendorOrReadOnly] 
