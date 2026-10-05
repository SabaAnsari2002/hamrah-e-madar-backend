from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditAdmin(admin.ModelAdmin):
    list_display=('action','user','object_type','object_id','created_at')
    list_filter=('action',)
    search_fields=('object_id','user__phone_number')
    readonly_fields=('user','action','object_type','object_id','ip_address','created_at')
    def has_add_permission(self,request): return False
    def has_change_permission(self,request,obj=None): return False
