from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from user.models import User

User = get_user_model()

class HomeOilDeliveryRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oil_delivery_requests', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Selected Oil Product")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    car_make = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    car_year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(help_text="Mileage of the car in kilometers")
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)  # Add email field for unregistered users
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.car_make} {self.car_model} ({self.car_year}) - {self.product.name if self.product else 'No product selected'}"
