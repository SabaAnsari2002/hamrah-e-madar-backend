from django.contrib import admin
from .models import *
class QuestionInline(admin.TabularInline):model=VisitQuestion;extra=0
@admin.register(PrenatalVisit)
class VisitAdmin(admin.ModelAdmin):list_display=('provider_name','pregnancy','provider_type','scheduled_at','status');search_fields=('provider_name','clinic_name','pregnancy__user__phone_number');list_filter=('provider_type','status');inlines=(QuestionInline,)
@admin.register(LabRecord)
class LabAdmin(admin.ModelAdmin):list_display=('title','pregnancy','performed_at','status');search_fields=('title','pregnancy__user__phone_number');list_filter=('status',)
@admin.register(UltrasoundRecord)
class UltrasoundAdmin(admin.ModelAdmin):list_display=('title','pregnancy','performed_at','gestational_week','center_name');search_fields=('title','center_name','pregnancy__user__phone_number')
@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):list_display=('name','pregnancy','is_active','start_date','end_date');search_fields=('name','pregnancy__user__phone_number');list_filter=('is_active',)
admin.site.register(MedicationIntake)
