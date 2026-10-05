from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.serializers import UserSerializer
from apps.pregnancies.serializers import PregnancySerializer
from apps.health.serializers import WeightSerializer,BloodPressureSerializer,BloodGlucoseSerializer
from apps.care.serializers import UserCareTaskSerializer
from apps.content.serializers import ArticleListSerializer
from .selectors import get_today_dashboard
class TodayDashboardView(APIView):
    pagination_class=None
    def get(self,request):
        data=get_today_dashboard(request.user)
        if not data:return Response({'user':UserSerializer(request.user).data,'pregnancy':None,'today_tasks':[],'health_summary':{'weight':None,'blood_pressure':None,'blood_glucose':None,'symptoms_count_today':0},'upcoming_events':[],'recommended_article':None})
        p,age,tasks,h,events,a=data
        return Response({'user':UserSerializer(request.user).data,'pregnancy':PregnancySerializer(p).data,'today_tasks':UserCareTaskSerializer(tasks,many=True).data,'health_summary':{'weight':WeightSerializer(h['weight']).data if h['weight'] else None,'blood_pressure':BloodPressureSerializer(h['blood_pressure']).data if h['blood_pressure'] else None,'blood_glucose':BloodGlucoseSerializer(h['blood_glucose']).data if h['blood_glucose'] else None,'symptoms_count_today':h['symptoms_count_today']},'upcoming_events':events,'recommended_article':ArticleListSerializer(a).data if a else None})
