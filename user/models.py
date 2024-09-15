from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        VENDOR = 'VENDOR', 'Vendor'
        CONSUMER = 'CONSUMER', 'Consumer'

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    paypal_address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

class ConsumerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.CONSUMER)

class Consumer(User):
    base_role = User.Role.CONSUMER
    consumer = ConsumerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for consumers"

class VendorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.VENDOR)

class Vendor(User):
    base_role = User.Role.VENDOR
    vendor = VendorManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for vendors"

class MileageRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mileage_records')
    current_mileage = models.IntegerField()
    next_change_mileage = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.next_change_mileage = self.current_mileage + 6000
        super().save(*args, **kwargs)
        self.delete_unnecessary_mileage()

    def delete_unnecessary_mileage(self):
        if self.user.mileage_records.count() > 1:
            self.user.mileage_records.exclude(pk=self.pk).delete()
