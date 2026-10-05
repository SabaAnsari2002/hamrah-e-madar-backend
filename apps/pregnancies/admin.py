from django.contrib import admin
from .models import Pregnancy,PregnancyWeek
@admin.register(Pregnancy)
class PregnancyAdmin(admin.ModelAdmin):list_display=('id','user','status','lmp_date','estimated_due_date','is_multiple','created_at');search_fields=('user__phone_number','id');list_filter=('status','is_multiple','provider_status');readonly_fields=('created_at','updated_at')
@admin.register(PregnancyWeek)
class PregnancyWeekAdmin(admin.ModelAdmin):list_display=('week_number','medical_reviewer','updated_at');ordering=('week_number',);search_fields=('baby_summary','mother_summary');readonly_fields=('created_at','updated_at')
