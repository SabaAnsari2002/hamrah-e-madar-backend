from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,OTPChallenge
@admin.register(User)
class HamrahUserAdmin(UserAdmin):
    model=User;ordering=('phone_number',);list_display=('phone_number','display_name','is_staff','is_active','date_joined');search_fields=('phone_number','display_name');list_filter=('is_staff','is_active');readonly_fields=('date_joined','last_login');fieldsets=((None,{'fields':('phone_number','password')}),('Profile',{'fields':('display_name',)}),('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),('Dates',{'fields':('last_login','date_joined')}));add_fieldsets=((None,{'classes':('wide',),'fields':('phone_number','display_name','password1','password2','is_staff','is_active')}),)
@admin.register(OTPChallenge)
class OTPAdmin(admin.ModelAdmin):list_display=('phone_number','expires_at','attempt_count','is_used','created_at');search_fields=('phone_number',);list_filter=('is_used',);readonly_fields=('code_hash','created_at')
