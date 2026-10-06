from django.contrib import admin
from django.utils.html import format_html

from .models import Pregnancy, PregnancyWeek


@admin.register(Pregnancy)
class PregnancyAdmin(admin.ModelAdmin):
    list_display = (
        'pregnancy_card',
        'user_card',
        'status_badge',
        'lmp_date',
        'estimated_due_date',
        'multiple_badge',
        'provider_status',
        'created_at',
    )
    list_display_links = ('pregnancy_card',)
    search_fields = ('user__phone_number', 'user__email', 'user__display_name', 'id')
    list_filter = ('status', 'is_multiple', 'provider_status', 'created_at')
    list_select_related = ('user',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('کاربر و وضعیت', {'fields': ('user', 'status')}),
        ('تاریخ‌گذاری بارداری', {'fields': ('lmp_date', 'estimated_due_date', 'actual_delivery_date')}),
        ('اطلاعات تکمیلی', {'fields': ('is_multiple', 'is_first_pregnancy', 'provider_status')}),
        ('اطلاعات سیستمی', {'fields': ('created_at', 'updated_at')}),
    )

    @admin.display(description='پرونده', ordering='id')
    def pregnancy_card(self, obj):
        short_id = str(obj.id).split('-')[0]
        return format_html(
            '<span class="hamrah-admin-identity">'
            '<span class="hamrah-admin-identity-avatar">P</span>'
            '<span class="hamrah-admin-identity-copy"><strong>بارداری {}</strong><small>{}</small></span>'
            '</span>',
            short_id,
            obj.id,
        )

    @admin.display(description='کاربر', ordering='user__display_name')
    def user_card(self, obj):
        label = obj.user.display_name or obj.user.email or obj.user.phone_number or 'بدون نام'
        secondary = obj.user.phone_number or obj.user.email or ''
        initial = (label[:1] or 'U').upper()
        return format_html(
            '<span class="hamrah-admin-identity">'
            '<span class="hamrah-admin-identity-avatar">{}</span>'
            '<span class="hamrah-admin-identity-copy"><strong>{}</strong><small>{}</small></span>'
            '</span>',
            initial,
            label,
            secondary,
        )

    @admin.display(description='وضعیت', ordering='status')
    def status_badge(self, obj):
        tone = {
            Pregnancy.Status.ACTIVE: 'success',
            Pregnancy.Status.COMPLETED: 'info',
            Pregnancy.Status.ENDED: 'neutral',
        }.get(obj.status, 'neutral')
        title = {
            Pregnancy.Status.ACTIVE: 'فعال',
            Pregnancy.Status.COMPLETED: 'تکمیل‌شده',
            Pregnancy.Status.ENDED: 'پایان‌یافته',
        }.get(obj.status, obj.get_status_display())
        return format_html('<span class="hamrah-status-badge {}">{}</span>', tone, title)

    @admin.display(description='نوع', ordering='is_multiple')
    def multiple_badge(self, obj):
        if obj.is_multiple:
            return format_html('<span class="hamrah-status-badge warning">چندقلویی</span>')
        return format_html('<span class="hamrah-status-badge neutral">تک‌قلویی</span>')


@admin.register(PregnancyWeek)
class PregnancyWeekAdmin(admin.ModelAdmin):
    list_display = ('week_number', 'medical_reviewer', 'updated_at')
    ordering = ('week_number',)
    search_fields = ('baby_summary', 'mother_summary', 'medical_reviewer')
    list_per_page = 40
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('هفته', {'fields': ('week_number',)}),
        ('رشد جنین', {'fields': ('baby_summary', 'baby_size_text', 'baby_weight_text')}),
        ('وضعیت مادر', {'fields': ('mother_summary',)}),
        ('راهنمای هفته', {'fields': ('nutrition_summary', 'activity_summary', 'care_summary', 'attention_summary')}),
        ('بازبینی پزشکی و منبع', {'fields': ('medical_reviewer', 'source_information')}),
        ('اطلاعات سیستمی', {'fields': ('created_at', 'updated_at')}),
    )
