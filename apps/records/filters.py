import django_filters
from .models import PrenatalVisit, LabRecord, UltrasoundRecord, Medication

class VisitFilter(django_filters.FilterSet):
    date_from=django_filters.IsoDateTimeFilter(field_name='scheduled_at',lookup_expr='gte')
    date_to=django_filters.IsoDateTimeFilter(field_name='scheduled_at',lookup_expr='lte')
    class Meta:model=PrenatalVisit;fields=['pregnancy','status','provider_type','date_from','date_to']
class LabFilter(django_filters.FilterSet):
    date_from=django_filters.IsoDateTimeFilter(field_name='performed_at',lookup_expr='gte')
    date_to=django_filters.IsoDateTimeFilter(field_name='performed_at',lookup_expr='lte')
    class Meta:model=LabRecord;fields=['pregnancy','status','date_from','date_to']
class UltrasoundFilter(django_filters.FilterSet):
    date_from=django_filters.IsoDateTimeFilter(field_name='performed_at',lookup_expr='gte')
    date_to=django_filters.IsoDateTimeFilter(field_name='performed_at',lookup_expr='lte')
    class Meta:model=UltrasoundRecord;fields=['pregnancy','gestational_week','date_from','date_to']
class MedicationFilter(django_filters.FilterSet):
    class Meta:model=Medication;fields=['pregnancy','is_active']
