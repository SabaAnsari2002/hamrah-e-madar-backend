from django.utils import timezone
from apps.pregnancies.models import Pregnancy
from apps.pregnancies.services import calculate_age
from apps.health.models import WeightMeasurement,BloodPressureMeasurement,BloodGlucoseMeasurement,SymptomEntry
from apps.records.models import PrenatalVisit,LabRecord,UltrasoundRecord
from apps.care.models import UserCareTask
from apps.content.models import Article
from apps.subscriptions.services import has_premium_access

def get_today_dashboard(user):
    p=Pregnancy.objects.filter(user=user,status=Pregnancy.Status.ACTIVE).first()
    if not p:return None
    today=timezone.localdate();now=timezone.now();age=calculate_age(p,today);week=max(1,min(40,age.gestational_age_weeks))
    premium=has_premium_access(user)
    tasks=(UserCareTask.objects.select_related('template').filter(pregnancy=p,scheduled_date__lte=today).exclude(status='SKIPPED').order_by('-scheduled_date','template__sort_order')[:3] if premium else [])
    health={'weight':None,'blood_pressure':None,'blood_glucose':None,'symptoms_count_today':0}
    events=[]
    if premium:
        health={'weight':WeightMeasurement.objects.filter(pregnancy=p).order_by('-measured_at').first(),'blood_pressure':BloodPressureMeasurement.objects.filter(pregnancy=p).order_by('-measured_at').first(),'blood_glucose':BloodGlucoseMeasurement.objects.filter(pregnancy=p).order_by('-measured_at').first(),'symptoms_count_today':SymptomEntry.objects.filter(pregnancy=p,occurred_at__date=today).count()}
        for v in PrenatalVisit.objects.filter(pregnancy=p,status='UPCOMING',scheduled_at__gte=now).order_by('scheduled_at')[:3]:events.append({'id':str(v.id),'type':'VISIT','title':v.provider_name,'scheduled_at':v.scheduled_at})
        for x in LabRecord.objects.filter(pregnancy=p,status='SCHEDULED',performed_at__gte=now).order_by('performed_at')[:3]:events.append({'id':str(x.id),'type':'LAB','title':x.title,'scheduled_at':x.performed_at})
        for x in UltrasoundRecord.objects.filter(pregnancy=p,performed_at__gte=now).order_by('performed_at')[:3]:events.append({'id':str(x.id),'type':'ULTRASOUND','title':x.title,'scheduled_at':x.performed_at})
    article=Article.objects.select_related('category').filter(is_published=True,week_from__lte=week,week_to__gte=week).order_by('-published_at').first()
    return p,age,list(tasks),health,sorted(events,key=lambda e:e['scheduled_at'])[:3],article
