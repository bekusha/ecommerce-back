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
        # send_order_notification(sender, instance, created, **kwargs)

        
@receiver(post_save, sender=Cart)
def create_order_for_product_delivery(sender, instance, created, **kwargs):
    if created:
        Order.objects.create(
            user=instance.user,
            order_type='product_delivery',
            # phone=instance.phone,
            # address=instance.address,
            # email=instance.email,
            # status=instance.status,
        )
        # send_order_notification(sender, instance, created, **kwargs)


@receiver(post_save, sender=Order)
def notify_status_change(sender, instance, **kwargs):
    print("notify_status_change")
    if instance.pk:  # ობიექტი უკვე არსებობს
        previous = sender.objects.get(pk=instance.pk)  # არსებული მონაცემის მიღება
        if previous.status != instance.status:  # თუ სტატუსი შეიცვალა
            message = {
                'order_id': instance.id,
                'status': instance.status,
                'order_type': instance.order_type,
                'phone': instance.phone,
                'address': instance.address,
                'email': instance.email,
            }
            instance.notify_user(message)
            print(f"Status changed and notification sent for order {instance.id}")


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    # შეტყობინება სტატუსის განახლების დროსაც
    message = {
        'order_id': instance.id,
        'status': instance.status,
        'order_type': instance.order_type,
        'phone': instance.phone,
        'address': instance.address,
        'email': instance.email,
    }

    if created:
        print(f"New order created: {instance.id}")
    else:
        print(f"Order updated: {instance.id} - New status: {instance.status}")

    print(f"Sending WebSocket notification: {message}")
    instance.notify_user(message)

# save phone number in user model from order
@receiver(post_save, sender=Order)
def save_phone_number(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.phone = instance.phone
        user.save()
        print(f"Phone number saved to user: {user.username}")
