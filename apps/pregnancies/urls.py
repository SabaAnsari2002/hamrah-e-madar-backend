from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router=DefaultRouter();router.register('pregnancies',PregnancyViewSet,basename='pregnancies')
urlpatterns=[path('',include(router.urls)),path('pregnancy/current/',CurrentPregnancyView.as_view()),path('pregnancy/weeks/',PregnancyWeekViewSet.as_view({'get':'list'})),path('pregnancy/weeks/<int:week>/',PregnancyWeekViewSet.as_view({'get':'retrieve'}))]
