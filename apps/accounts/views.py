from django.contrib.auth.models import update_last_login
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from apps.audit.models import AuditLog
from apps.audit.services import audit, client_ip
from .serializers import *
from .services import request_otp, verify_otp, delete_account

class OTPRequestView(APIView):
    permission_classes=[permissions.AllowAny]
    @extend_schema(request=OTPRequestSerializer,responses={200:dict})
    def post(self,request):
        s=OTPRequestSerializer(data=request.data);s.is_valid(raise_exception=True);request_otp(s.validated_data['phone_number'],client_ip(request));return Response({'message':'Verification code generated.','expires_in_seconds':120,'resend_after_seconds':60})
class OTPVerifyView(APIView):
    permission_classes=[permissions.AllowAny]
    @extend_schema(request=OTPVerifySerializer,responses={200:dict})
    def post(self,request):
        s=OTPVerifySerializer(data=request.data);s.is_valid(raise_exception=True);user=verify_otp(**s.validated_data);update_last_login(None,user);refresh=RefreshToken.for_user(user);AuditLog.objects.create(user=user,action=AuditLog.Action.LOGIN,object_type='User',object_id=str(user.id),ip_address=client_ip(request));return Response({'access':str(refresh.access_token),'refresh':str(refresh),'user':UserSerializer(user).data})
class LogoutView(APIView):
    def post(self,request):
        s=LogoutSerializer(data=request.data);s.is_valid(raise_exception=True)
        try: RefreshToken(s.validated_data['refresh']).blacklist()
        except Exception: pass
        return Response(status=status.HTTP_204_NO_CONTENT)
class MeView(APIView):
    def get(self,request): return Response(UserSerializer(request.user).data)
    def patch(self,request):
        s=UserUpdateSerializer(request.user,data=request.data,partial=True);s.is_valid(raise_exception=True);s.save();return Response(UserSerializer(request.user).data)
    def delete(self,request):
        audit(request,AuditLog.Action.ACCOUNT_DELETE,'User',request.user.id);delete_account(request.user);return Response(status=status.HTTP_204_NO_CONTENT)
