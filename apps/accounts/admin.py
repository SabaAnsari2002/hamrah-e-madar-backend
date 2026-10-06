from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import OTPChallenge, User


@admin.register(User)
class HamrahUserAdmin(UserAdmin):
    model = User
    ordering = ('-date_joined',)
    list_display = (
        'identity_card',
        'phone_number',
        'email',
        'provider_badge',
        'staff_badge',
        'active_badge',
        'date_joined',
    )
    list_display_links = ('identity_card',)
    search_fields = ('phone_number', 'display_name', 'email', 'google_sub')
    list_filter = ('auth_provider', 'is_staff', 'is_active', 'date_joined')
    list_per_page = 25
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        ('اطلاعات ورود', {'fields': ('phone_number', 'email', 'password')}),
        ('پروفایل', {'fields': ('display_name', 'avatar_url', 'auth_provider', 'google_sub')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('ایجاد کاربر', {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'display_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    @admin.display(description='کاربر', ordering='display_name')
    def identity_card(self, obj):
        label = obj.display_name or obj.email or obj.phone_number or 'بدون نام'
        secondary = obj.phone_number or obj.email or str(obj.id)
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

    @admin.display(description='روش ورود', ordering='auth_provider')
    def provider_badge(self, obj):
        if obj.auth_provider == User.AuthProvider.GOOGLE:
            return format_html('<span class="hamrah-status-badge info">Google</span>')
        return format_html('<span class="hamrah-status-badge neutral">موبایل</span>')

    @admin.display(description='مدیر', ordering='is_staff')
    def staff_badge(self, obj):
        if obj.is_staff:
            return format_html('<span class="hamrah-status-badge info">Staff</span>')
        return format_html('<span class="hamrah-status-badge neutral">کاربر</span>')

    @admin.display(description='وضعیت', ordering='is_active')
    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="hamrah-status-badge success">فعال</span>')
        return format_html('<span class="hamrah-status-badge danger">غیرفعال</span>')


@admin.register(OTPChallenge)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'expires_at', 'attempt_count', 'used_badge', 'created_at')
    search_fields = ('phone_number',)
    list_filter = ('is_used', 'created_at')
    list_per_page = 30
    readonly_fields = ('code_hash', 'created_at')

    @admin.display(description='وضعیت', ordering='is_used')
    def used_badge(self, obj):
        if obj.is_used:
            return format_html('<span class="hamrah-status-badge neutral">استفاده‌شده</span>')
        return format_html('<span class="hamrah-status-badge success">فعال</span>')
