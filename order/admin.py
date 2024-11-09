# order/admin.py
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_type', 'phone', 'address', 'email', 'ordered_at_georgian', 'status')
    list_filter = ('status', 'order_type')
    search_fields = ('user__username', 'email', 'phone')
    actions = ['mark_as_in_progress', 'mark_as_delivered']

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = 'Mark selected orders as In Progress'

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Mark selected orders as Delivered'
