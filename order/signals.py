# order/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from cart.models import Cart
from .models import Order, SavedOrder
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
            phone=instance.phone,
            address=instance.address,
            email=instance.email,
            status=instance.status,
        )
        # send_order_notification(sender, instance, created, **kwargs)

previous_status = {}
@receiver(pre_save, sender=Order)
def cache_previous_status(sender, instance, **kwargs):
    """ შეკვეთის სტატუსი შენახვამდე ვინახავთ, რომ შევადაროთ post_save-ში """
    if instance.pk:
        try:
            previous_status[instance.pk] = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            previous_status[instance.pk] = None


@receiver(post_save, sender=Order)
def notify_status_change(sender, instance, **kwargs):
        old_status = previous_status.get(instance.pk, None)
        if old_status != instance.status:    
            message = {
                'order_id': instance.id,
                'status': instance.status,
                'payment_status': instance.payment_status,  
                'order_type': instance.order_type,
                'phone': instance.phone,
                'address': instance.address,
                'email': instance.email,
                'courier_name': instance.courier_name if instance.courier_name else "",
                'courier_phone': instance.courier_phone if instance.courier_phone else "",
                'delivery_time': instance.delivery_time.strftime('%Y-%m-%d %H:%M:%S') if instance.delivery_time else "",
            }
            instance.notify_user(message)
            print(f"🚀 WebSocket notification sent for order {instance.id} - Status: {instance.status}, Payment: {instance.payment_status}")


@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    # შეტყობინება სტატუსის განახლების დროსაც
    message = {
        'order_id': instance.id,
        'status': instance.status,
        'order_type': instance.order_type,
        'payment_status': instance.payment_status,  # ✅ დავამატოთ გადახდის სტატუსი
        'phone': instance.phone,
        'address': instance.address,
        'email': instance.email,
        'courier_name': instance.courier_name if instance.courier_name else "",
        'courier_phone': instance.courier_phone if instance.courier_phone else "",
        'delivery_time': instance.delivery_time.strftime('%Y-%m-%d %H:%M:%S') if instance.delivery_time else "",
    }

    if created:
        print(f"New order created: {instance.id}")
    else:
        print(f"♻️ Order updated: {instance.id} - New status: {instance.status}, Payment: {instance.payment_status}")

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

@receiver(post_save, sender=Order)
def save_order_data(sender, instance, **kwargs):
    if instance.status == 'delivered' or instance.payment_status == 'paid':
        SavedOrder.objects.create(
            order_data={
                "order_id": instance.id,
                "date": instance.ordered_at.strftime('%Y-%m-%d %H:%M:%S'),  # შეკვეთის თარიღი
                "order_type": instance.order_type,  # შეკვეთის ტიპი (მაგ. ნავთის მიწოდება)
                "status": instance.status,  # სტატუსი
                "payment_status": instance.payment_status,  # გადახდის სტატუსი
                "customer": {
                    "id": instance.user.id,
                    "username": instance.user.username,
                    "phone": instance.phone,
                    "email": instance.email,
                },
                "delivery": {
                    "address": instance.address,
                    "courier_name": instance.courier_name,
                    "courier_phone": instance.courier_phone,
                    "delivery_time": instance.delivery_time.strftime('%Y-%m-%d %H:%M:%S') if instance.delivery_time else None,
                },
                "mileage": instance.mileage,  # მანქანის გარბენი
                "products": [
                    {
                        "product_id": item.product.id,
                        "name": item.product.name,
                        "total_price": float(item.total_price),
                        "quantity": item.quantity,
                         "total_price": float(item.total_price),
                    }
                    for item in instance.order_items.all()
                ]
            }
        )
        print(f"✅ Saved order created for order {instance.id}")


