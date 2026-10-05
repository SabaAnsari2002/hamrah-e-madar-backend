from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from config.ownership import PregnancyOwnedQuerysetMixin
from .models import *
from .serializers import *
from .filters import WeightFilter,BloodPressureFilter,BloodGlucoseFilter,SymptomFilter

class MeasurementViewSet(PregnancyOwnedQuerysetMixin,viewsets.ModelViewSet):
    filterset_fields=['pregnancy'];ordering_fields=['measured_at','created_at'];ordering=['-measured_at']
class WeightViewSet(MeasurementViewSet): queryset=WeightMeasurement.objects.select_related('pregnancy').all();serializer_class=WeightSerializer;filterset_class=WeightFilter
class BloodPressureViewSet(MeasurementViewSet): queryset=BloodPressureMeasurement.objects.select_related('pregnancy').all();serializer_class=BloodPressureSerializer;filterset_class=BloodPressureFilter
class BloodGlucoseViewSet(MeasurementViewSet): queryset=BloodGlucoseMeasurement.objects.select_related('pregnancy').all();serializer_class=BloodGlucoseSerializer;filterset_class=BloodGlucoseFilter
class SymptomViewSet(PregnancyOwnedQuerysetMixin,viewsets.ModelViewSet):
    queryset=SymptomEntry.objects.select_related('pregnancy').all();serializer_class=SymptomSerializer;filterset_class=SymptomFilter;ordering_fields=['occurred_at','created_at'];ordering=['-occurred_at']

class HealthSummaryView(APIView):
    def get(self,request):
        p=request.user.pregnancies.filter(status='ACTIVE').first()
        if not p:return Response({'weight':None,'blood_pressure':None,'blood_glucose':None,'symptoms_count_today':0})
        w=WeightMeasurement.objects.filter(pregnancy=p).order_by('-measured_at').first();bp=BloodPressureMeasurement.objects.filter(pregnancy=p).order_by('-measured_at').first();g=BloodGlucoseMeasurement.objects.filter(pregnancy=p).order_by('-measured_at').first();today=timezone.localdate();count=SymptomEntry.objects.filter(pregnancy=p,occurred_at__date=today).count()
        return Response({'weight':WeightSerializer(w).data if w else None,'blood_pressure':BloodPressureSerializer(bp).data if bp else None,'blood_glucose':BloodGlucoseSerializer(g).data if g else None,'symptoms_count_today':count})
