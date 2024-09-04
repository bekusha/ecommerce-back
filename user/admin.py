from django.contrib import admin

from .models import User, MileageRecord
admin.site.register(User)
admin.site.register(MileageRecord)
