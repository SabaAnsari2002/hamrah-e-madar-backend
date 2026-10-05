from dataclasses import dataclass
from datetime import date,timedelta
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Pregnancy

@dataclass(frozen=True)
class PregnancyAge:
    gestational_age_weeks:int; gestational_age_days:int; total_gestational_days:int; estimated_due_date:date; days_remaining:int; current_trimester:str

def calculate_age(pregnancy, today=None):
    today=today or date.today()
    if pregnancy.lmp_date: lmp=pregnancy.lmp_date; due=pregnancy.estimated_due_date or lmp+timedelta(days=280)
    elif pregnancy.estimated_due_date: due=pregnancy.estimated_due_date; lmp=due-timedelta(days=280)
    else: raise ValidationError({'lmp_date':['Either lmp_date or estimated_due_date is required.']})
    total=max(0,(today-lmp).days); weeks,days=divmod(total,7)
    trimester='FIRST' if weeks<14 else 'SECOND' if weeks<28 else 'THIRD'
    return PregnancyAge(weeks,days,total,due,max(0,(due-today).days),trimester)

@transaction.atomic
def create_pregnancy(user, **data):
    if data.get('status',Pregnancy.Status.ACTIVE)==Pregnancy.Status.ACTIVE:
        if Pregnancy.objects.select_for_update().filter(user=user,status=Pregnancy.Status.ACTIVE).exists(): raise ValidationError({'status':['Only one active pregnancy is allowed.']})
    if not data.get('lmp_date') and not data.get('estimated_due_date'): raise ValidationError({'lmp_date':['Either lmp_date or estimated_due_date is required.']})
    if data.get('lmp_date') and not data.get('estimated_due_date'): data['estimated_due_date']=data['lmp_date']+timedelta(days=280)
    return Pregnancy.objects.create(user=user,**data)
