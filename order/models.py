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

    PAYMENT_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
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
    mileage = models.PositiveIntegerField(help_text="Mileage of the car in kilometers" , null=True, blank=True) 
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='not_paid')
    def __str__(self):
        return f"{self.get_order_type_display()} Order for {self.user.username} - Status: {self.status} - Payment: {self.payment_status}"
    
    def notify_user(self):
        """
        ცვლილებების შემთხვევაში ვაგზავნით WebSocket შეტყობინებას.
        """
        channel_layer = get_channel_layer()
        group_name = f"user_{self.user.id}_{self.user.device_id}"

        message = {
            'order_id': self.id,
            'status': self.status,
            'payment_status': self.payment_status,
            'order_type': self.order_type,
            'phone': self.phone,
            'address': self.address,
            'email': self.email,
            'courier_name': self.courier_name,  # ✅ ახლა ეს იგზავნება WebSocket-ით
            'courier_phone': self.courier_phone,  # ✅ იგზავნება WebSocket-ით
            'delivery_time': self.delivery_time.strftime('%Y-%m-%d %H:%M:%S') if self.delivery_time else '',  # ✅ სწორი ფორმატით
            'mileage': self.mileage,
        }

        print("🚀 Sending WebSocket message:", message)

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'order_update',
                **message,
            }
        )

    def save(self, *args, **kwargs):
        """
        **Admin Panel-იდან ნებისმიერი ცვლილება გამოიწვევს WebSocket შეტყობინებას.**
        """
        super().save(*args, **kwargs)  # ✅ ჩვეულებრივად ვინახავთ
        self.notify_user()
    

    # def save(self, *args, **kwargs):
    #     """
    #     თუ შეკვეთის სტატუსი `delivered` გახდა, წაშალოს OrderItem-ები და Order-ი.
    #     `SavedOrder` დარჩება.
    #     """
    #     if self.pk:  # თუ Order უკვე არსებობს
    #         old_status = Order.objects.get(pk=self.pk).status
    #         if old_status != "delivered" and self.status == "delivered":
    #             # წაშალე OrderItem-ები
    #             self.order_items.all().delete()
    #             # Order-ი წავშალოთ
    #             self.delete()
    #             return  # არ განვაახლოთ, რადგან Order აღარ არსებობს

    #     super().save(*args, **kwargs)

    @property
    def ordered_at_georgian(self):
        georgian_timezone = pytz.timezone('Asia/Tbilisi')
        return self.ordered_at.astimezone(georgian_timezone)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    recommended_quantity = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order {self.order.id}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
class SavedOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='saved_orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_orders')  
    oil_used = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Selected Oil Product")
    created_at = models.DateTimeField(auto_now_add=True)
    mileage = models.PositiveIntegerField(help_text="Mileage of the car in kilometers" , null=True, blank=True)
     