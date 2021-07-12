from django.contrib import admin
from .models import ExpoToken, UserNotifications

# Register your models here.
admin.site.register(ExpoToken)
admin.site.register(UserNotifications)