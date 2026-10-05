from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTPChallenge


@admin.register(User)
class HamrahUserAdmin(UserAdmin):
    model = User
    ordering = ('date_joined',)
    list_display = ('display_name', 'phone_number', 'email', 'auth_provider', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('phone_number', 'display_name', 'email', 'google_sub')
    list_filter = ('auth_provider', 'is_staff', 'is_active')
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Profile', {'fields': ('display_name', 'avatar_url', 'auth_provider', 'google_sub')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('phone_number', 'email', 'display_name', 'password1', 'password2', 'is_staff', 'is_active')}),
    )


@admin.register(OTPChallenge)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'expires_at', 'attempt_count', 'is_used', 'created_at')
    search_fields = ('phone_number',)
    list_filter = ('is_used',)
    readonly_fields = ('code_hash', 'created_at')
