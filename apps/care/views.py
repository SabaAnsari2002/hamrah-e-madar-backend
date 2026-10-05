from django.utils import timezone
from rest_framework import mixins,viewsets
from .models import UserCareTask
from apps.subscriptions.permissions import HasPremiumAccess
from .serializers import UserCareTaskSerializer
class UserCareTaskViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    permission_classes=[HasPremiumAccess]
    serializer_class=UserCareTaskSerializer;filterset_fields=['status','scheduled_date'];ordering_fields=['scheduled_date'];ordering=['scheduled_date']
    def get_queryset(self):return UserCareTask.objects.select_related('pregnancy','template').filter(pregnancy__user=self.request.user)
    def perform_update(self,serializer):
        status=serializer.validated_data.get('status',serializer.instance.status);serializer.save(completed_at=timezone.now() if status==UserCareTask.Status.COMPLETED else None)
