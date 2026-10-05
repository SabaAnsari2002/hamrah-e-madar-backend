from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
urlpatterns=[path('auth/otp/request/',OTPRequestView.as_view()),path('auth/otp/verify/',OTPVerifyView.as_view()),path('auth/token/refresh/',TokenRefreshView.as_view()),path('auth/logout/',LogoutView.as_view()),path('me/',MeView.as_view())]
