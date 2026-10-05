from .models import AuditLog

def client_ip(request):
    forwarded=request.META.get('HTTP_X_FORWARDED_FOR','').split(',')[0].strip()
    return forwarded or request.META.get('REMOTE_ADDR')

def audit(request, action, object_type='', object_id=''):
    AuditLog.objects.create(user=request.user if getattr(request,'user',None) and request.user.is_authenticated else None, action=action, object_type=object_type, object_id=str(object_id)[:80], ip_address=client_ip(request))
