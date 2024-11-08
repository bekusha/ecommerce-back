from django.contrib import admin

from .models import OilChangeDelivery

class OilChangeDeliveryAdmin(admin.ModelAdmin):
    fields = ('user', 'phone', 'address', 'email',  'ordered_at',)
    readonly_fields = ('ordered_at',)
admin.site.register(OilChangeDelivery, OilChangeDeliveryAdmin)