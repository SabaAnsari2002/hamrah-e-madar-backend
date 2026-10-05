from datetime import timedelta
from django.db import transaction
from .models import CareTaskTemplate,UserCareTask
from apps.pregnancies.services import calculate_age

@transaction.atomic
def generate_care_tasks(pregnancy, week_number=None):
    week=week_number or calculate_age(pregnancy).gestational_age_weeks
    week=max(1,min(40,week)); base=pregnancy.lmp_date or pregnancy.estimated_due_date-timedelta(days=280);scheduled=base+timedelta(days=(week-1)*7)
    created=[]
    for template in CareTaskTemplate.objects.filter(is_active=True,week_from__lte=week,week_to__gte=week).order_by('sort_order'):
        obj,_=UserCareTask.objects.get_or_create(pregnancy=pregnancy,template=template,scheduled_date=scheduled);created.append(obj)
    return created
