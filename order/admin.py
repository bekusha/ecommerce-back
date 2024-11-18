# order/admin.py
from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_type', 'phone', 'address', 'email', 'ordered_at_georgian', 'status', 'order_items_summary')
    list_filter = ('status', 'order_type')
    search_fields = ('user__username', 'email', 'phone')
    actions = ['mark_as_in_progress', 'mark_as_delivered']

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = 'Mark selected orders as In Progress'

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Mark selected orders as Delivered'

    def order_items_summary(self, obj):
        items = obj.order_items.all()
        if not items.exists():
            return 'No items'
        return ' , '.join([f'{item.product.name} რაოდენობა:({item.quantity})/' for item in items])

    order_items_summary.short_description = 'Order Items'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')