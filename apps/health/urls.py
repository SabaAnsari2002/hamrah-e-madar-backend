from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router=DefaultRouter();router.register('health/weights',WeightViewSet,basename='weights');router.register('health/blood-pressures',BloodPressureViewSet,basename='blood-pressures');router.register('health/blood-glucose',BloodGlucoseViewSet,basename='blood-glucose');router.register('health/symptoms',SymptomViewSet,basename='symptoms')
urlpatterns=[path('',include(router.urls)),path('health/summary/',HealthSummaryView.as_view())]
