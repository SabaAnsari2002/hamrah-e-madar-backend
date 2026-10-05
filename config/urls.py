from django.contrib import admin
from django.urls import include,path
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
urlpatterns=[
    path('admin/',admin.site.urls),
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='docs'),
    path('api/v1/',include('apps.accounts.urls')),
    path('api/v1/',include('apps.pregnancies.urls')),
    path('api/v1/',include('apps.health.urls')),
    path('api/v1/',include('apps.records.urls')),
    path('api/v1/',include('apps.care.urls')),
    path('api/v1/',include('apps.content.urls')),
    path('api/v1/',include('apps.reminders.urls')),
    path('api/v1/',include('apps.dashboard.urls')),
]
