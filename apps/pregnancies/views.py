from rest_framework import generics,viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.audit.models import AuditLog
from .models import Pregnancy,PregnancyWeek
from .serializers import PregnancySerializer,PregnancyWeekSerializer
class PregnancyViewSet(viewsets.ModelViewSet):
    serializer_class=PregnancySerializer;http_method_names=['get','post','patch','head','options']
    def get_queryset(self): return Pregnancy.objects.filter(user=self.request.user)
    def perform_create(self,serializer):
        obj=serializer.save();AuditLog.objects.create(user=self.request.user,action=AuditLog.Action.PREGNANCY_CREATE,object_type='Pregnancy',object_id=str(obj.id))
class CurrentPregnancyView(generics.RetrieveAPIView):
    serializer_class=PregnancySerializer
    def get_object(self): return get_object_or_404(Pregnancy,user=self.request.user,status=Pregnancy.Status.ACTIVE)
class PregnancyWeekViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=PregnancyWeekSerializer;queryset=PregnancyWeek.objects.all().order_by('week_number');lookup_field='week_number';lookup_url_kwarg='week'
