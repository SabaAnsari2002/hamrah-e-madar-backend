from django.contrib import admin
from .models import CareTaskTemplate,UserCareTask
@admin.register(CareTaskTemplate)
class TemplateAdmin(admin.ModelAdmin):list_display=('title','week_from','week_to','category','is_active','sort_order');search_fields=('title','description');list_filter=('category','is_active');ordering=('week_from','sort_order')
@admin.register(UserCareTask)
class TaskAdmin(admin.ModelAdmin):list_display=('pregnancy','template','scheduled_date','status','completed_at');list_filter=('status','scheduled_date');search_fields=('pregnancy__user__phone_number','template__title')
