from django.contrib import admin
from .models import Reminder
@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):list_display=('title','user','type','scheduled_at','is_completed');search_fields=('title','user__phone_number');list_filter=('type','is_completed')
