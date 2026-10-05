from rest_framework import viewsets
from .models import Reminder
from .serializers import ReminderSerializer
from .filters import ReminderFilter
from apps.subscriptions.permissions import HasPremiumAccess
class ReminderViewSet(viewsets.ModelViewSet):
    permission_classes=[HasPremiumAccess]
    serializer_class=ReminderSerializer;filterset_class=ReminderFilter;ordering_fields=['scheduled_at','created_at'];ordering=['scheduled_at']
    def get_queryset(self):return Reminder.objects.select_related('pregnancy').filter(user=self.request.user)
    def perform_create(self,serializer):serializer.save(user=self.request.user)
