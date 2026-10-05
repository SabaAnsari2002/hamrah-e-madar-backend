from rest_framework.exceptions import ValidationError

class PregnancyOwnedQuerysetMixin:
    """Scopes objects through pregnancy.user and validates ownership on writes."""
    def get_queryset(self):
        return super().get_queryset().filter(pregnancy__user=self.request.user)

    def _validate_pregnancy(self, serializer):
        pregnancy = serializer.validated_data.get('pregnancy')
        if pregnancy is not None and pregnancy.user_id != self.request.user.id:
            raise ValidationError({'pregnancy':['Invalid pregnancy.']})
        return pregnancy

    def perform_create(self, serializer):
        pregnancy = self._validate_pregnancy(serializer)
        if pregnancy is None:
            raise ValidationError({'pregnancy':['This field is required.']})
        serializer.save()

    def perform_update(self, serializer):
        self._validate_pregnancy(serializer)
        serializer.save()
