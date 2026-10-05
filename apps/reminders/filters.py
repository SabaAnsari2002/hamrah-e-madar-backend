import django_filters
from .models import Reminder
class ReminderFilter(django_filters.FilterSet):
    date_from=django_filters.IsoDateTimeFilter(field_name='scheduled_at',lookup_expr='gte')
    date_to=django_filters.IsoDateTimeFilter(field_name='scheduled_at',lookup_expr='lte')
    class Meta:model=Reminder;fields=['type','is_completed','pregnancy','date_from','date_to']
