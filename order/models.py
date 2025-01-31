from django.db import models
from django.contrib.auth import get_user_model
import pytz
from cart.models import Cart
from product.models import Product
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    email = models.EmailField(null=True, blank=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    courier_name = models.CharField(max_length=100, null=True, blank=True)
    courier_phone = models.CharField(max_length=10, null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_order_type_display()} Order for {self.user.username} - Status: {self.status}"
    
    def notify_user(self, message):
            channel_layer = get_channel_layer()
            group_name = f"user_{self.user.id}_{self.user.device_id}"
            # Convert datetime to string
            delivery_time_str = self.delivery_time.strftime('%Y-%m-%d %H:%M:%S') if self.delivery_time else ""
            print("Final Message Data:", {
            'order_id': message['order_id'],
            'status': message['status'],
            'order_type': message['order_type'],
            'phone': message['phone'],
            'address': message['address'],
            'email': message['email'],
            'courier_name': self.courier_name,  # დავამატოთ Order-ის ატრიბუტები
            'courier_phone': self.courier_phone,
            'delivery_time': self.delivery_time,
        })
        
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'order_update',
                    'order_id': message['order_id'],
                    'status': message['status'],
                    'order_type': message['order_type'],
                    'phone': message['phone'],
                    'address': message['address'],
                    'email': message['email'],
                    'courier_name': message.get('courier_name', ''),
                    'courier_phone': message.get('courier_phone', ''),
                    'delivery_time': message.get('delivery_time', ''),
                }
            )
    



    @property
    def ordered_at_georgian(self):
        georgian_timezone = pytz.timezone('Asia/Tbilisi')
        return self.ordered_at.astimezone(georgian_timezone)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order {self.order.id}"

    @property
    def total_price(self):
        return self.product.price * self.quantity