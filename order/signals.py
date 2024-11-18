# order/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Cart
from .models import Order
from oilchangedelivery.models import OilChangeDelivery

@receiver(post_save, sender=OilChangeDelivery)
def create_order_from_oil_change(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            user=instance.user,
            order_type='oil_change',
            phone=instance.phone,
            address=instance.address,
            email=instance.email,
            status=instance.status,
        )

        
@receiver(post_save, sender=Cart)
def create_order_for_product_delivery(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            user=instance.user,
            order_type='product_delivery',
            phone=instance.phone,
            address=instance.address,
            email=instance.email,
            status=instance.status,
        )