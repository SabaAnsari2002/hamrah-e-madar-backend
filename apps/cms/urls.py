from django.urls import path
from .views import CmsDashboardView

urlpatterns = [
    path('', CmsDashboardView.as_view(), name='cms-dashboard'),
]
