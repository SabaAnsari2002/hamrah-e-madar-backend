import django_filters
from .models import WeightMeasurement,BloodPressureMeasurement,BloodGlucoseMeasurement,SymptomEntry

class MeasurementFilter(django_filters.FilterSet):
    date_from=django_filters.IsoDateTimeFilter(field_name='measured_at',lookup_expr='gte')
    date_to=django_filters.IsoDateTimeFilter(field_name='measured_at',lookup_expr='lte')
class WeightFilter(MeasurementFilter):
    class Meta:model=WeightMeasurement;fields=['pregnancy','date_from','date_to']
class BloodPressureFilter(MeasurementFilter):
    class Meta:model=BloodPressureMeasurement;fields=['pregnancy','date_from','date_to']
class BloodGlucoseFilter(MeasurementFilter):
    class Meta:model=BloodGlucoseMeasurement;fields=['pregnancy','measurement_type','date_from','date_to']
class SymptomFilter(django_filters.FilterSet):
    date_from=django_filters.IsoDateTimeFilter(field_name='occurred_at',lookup_expr='gte');date_to=django_filters.IsoDateTimeFilter(field_name='occurred_at',lookup_expr='lte')
    class Meta:model=SymptomEntry;fields=['pregnancy','severity','symptom_type','date_from','date_to']
