from django.urls import path
from .views import CategoryListAPIView, MyProductsAPIView, ProductListCreateAPIView, ProductDetailAPIView, ProductsByVendorAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
     path('categories/', CategoryListAPIView.as_view(), name='category-list'),
      path('my/', MyProductsAPIView.as_view(), name='my-products'),  
      path('products/by_vendor/<int:vendor_id>/', ProductsByVendorAPIView.as_view(), name='products-by-vendor'),
]