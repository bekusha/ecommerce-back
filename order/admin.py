# order/admin.py
from django.contrib import admin
from .models import Order, OrderItem, SavedOrder


class OrderItemInline(admin.TabularInline):  # ან admin.StackedInline
    model = OrderItem
    extra = 0  # თავიდან ცარიელი OrderItem არ გამოჩნდეს
    readonly_fields = ('product', 'recommended_quantity', 'total_price','liter')

    def liter(self, obj):
        return f"{obj.product.liter} L" if obj.product and obj.product.liter else "N/A"

@admin.register(Order)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_type', 'phone', 'address', 'email', 'ordered_at_georgian', 'status', 'order_items_summary', 'courier_name', 'courier_phone','delivery_time', 'payment_status')
    list_filter = ('status', 'order_type')
    search_fields = ('user__username', 'email', 'phone')
    inlines = [OrderItemInline]
    

    def mark_as_in_progress(self, request, queryset):
        for order in queryset:
            order.status = 'in_progress'
            order.save()  # save() გამოძახება ინდივიდუალურად, რათა post_save სიგნალი ჩაირთოს

    # mark_as_in_progress.short_description = 'Mark selected orders as In Progress'

    def mark_as_delivered(self, request, queryset):
        for order in queryset:
            order.status = 'delivered'
            order.save()  # save() გამოძახება ინდივიდუალურად, რათა post_save სიგნალი ჩაირთოს

    # mark_as_delivered.short_description = 'Mark selected orders as Delivered'


    def order_items_summary(self, obj):
        items = obj.order_items.all()
        if not items.exists():
            return 'No items'
        return ' , '.join([f'{item.product.name} რაოდენობა:({item.quantity})/' for item in items])

    order_items_summary.short_description = 'Order Items'



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')


# @admin.register(SavedOrder)
# class SavedOrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'order', 'mileage', 'oil_used', 'created_at')