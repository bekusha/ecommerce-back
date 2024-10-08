from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
import pytz

User = get_user_model()

class OilChangeDelivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oil_change_deliveries')
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    ordered_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Oil Change Delivery for {self.user.username} - {self.product.name}"
    
    # def get_ordered_at_georgian_time(self):
    #     georgian_timezone = pytz.timezone('Asia/Tbilisi')
    #     ordered_at_georgian_time = self.ordered_at.astimezone(georgian_timezone)
    #     return ordered_at_georgian_time

    @property
    def ordered_at_georgian(self):
        georgian_timezone = pytz.timezone('Asia/Tbilisi')
        return self.ordered_at.astimezone(georgian_timezone)
