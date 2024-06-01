from django.contrib import admin
from .models import HomeOilDeliveryRequest

@admin.register(HomeOilDeliveryRequest)
class HomeOilDeliveryRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'car_make', 'car_model', 'car_year', 'product', 'status', 'created_at')
    list_filter = ('status', 'car_make', 'car_year', 'product')
    search_fields = ('first_name', 'last_name', 'phone_number', 'address', 'product__name')

