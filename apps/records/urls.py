from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import *
router=DefaultRouter();router.register('visits',PrenatalVisitViewSet,basename='visits');router.register('labs',LabRecordViewSet,basename='labs');router.register('ultrasounds',UltrasoundRecordViewSet,basename='ultrasounds');router.register('medications',MedicationViewSet,basename='medications');router.register('visit-questions',VisitQuestionDetailViewSet,basename='visit-questions')
urlpatterns=[path('',include(router.urls)),path('records/summary/',RecordsSummaryView.as_view())]
