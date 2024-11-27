from django.db import models
from django.contrib.auth import get_user_model
import pytz
from cart.models import Cart
from product.models import Product

User = get_user_model()

class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ('oil_change', 'Oil Change'),
        ('product_delivery', 'Product Delivery'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='oil_change')
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.get_order_type_display()} Order for {self.user.username} - Status: {self.status}"

    @property
    def ordered_at_georgian(self):
        georgian_timezone = pytz.timezone('Asia/Tbilisi')
        return self.ordered_at.astimezone(georgian_timezone)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name if self.product else 'No Product'} x {self.quantity} for Order {self.order.id}"

    @property
    def total_price(self):
        return self.product.price * self.quantity if self.product else 0

