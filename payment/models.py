from django.db import models
from user.models import User
from product.models import Product
from decimal import Decimal

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    admin_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vendor_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payer_details = models.JSONField()

    def __str__(self):
        return f"Transaction {self.transaction_id} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Calculating amounts only on creation
            self.admin_amount = self.total_amount * Decimal('0.10')
            self.vendor_amount = self.total_amount * Decimal('0.90')
        super().save(*args, **kwargs)

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_transaction = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} at {self.price_at_transaction} each"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.product.quantity >= self.quantity:  
                self.product.quantity -= self.quantity
                self.product.save()
            else:
                
                raise ValueError("Not enough stock to complete the transaction.")
        super(TransactionItem, self).save(*args, **kwargs)

class Payout(models.Model):
    vendor_email = models.EmailField(max_length=254)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')  # Options might include 'Pending', 'Completed', 'Failed'
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor_email} - {self.status}"