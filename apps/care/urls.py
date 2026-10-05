from django.urls import include,path
from rest_framework.routers import DefaultRouter
from .views import UserCareTaskViewSet
router=DefaultRouter();router.register('care/tasks',UserCareTaskViewSet,basename='care-tasks');urlpatterns=[path('',include(router.urls))]
