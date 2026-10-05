from datetime import timedelta,time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User
from apps.pregnancies.models import Pregnancy,PregnancyWeek
from apps.health.models import WeightMeasurement,BloodPressureMeasurement,BloodGlucoseMeasurement,SymptomEntry
from apps.records.models import PrenatalVisit,VisitQuestion,LabRecord,UltrasoundRecord,Medication
from apps.care.models import CareTaskTemplate,UserCareTask
from apps.content.models import ArticleCategory,Article
from apps.reminders.models import Reminder

class Command(BaseCommand):
    help='Create deterministic, clearly labeled demo data for local development.'
    def handle(self,*args,**opts):
        now=timezone.now();today=timezone.localdate();lmp=today-timedelta(days=171);due=lmp+timedelta(days=280)
        phone=User.objects.normalize_phone('09120000000');user,_=User.objects.get_or_create(phone_number=phone,defaults={'display_name':'Sara'}); user.display_name='Sara';user.save(update_fields=['display_name'])
        Pregnancy.objects.filter(user=user).delete()
        p=Pregnancy.objects.create(user=user,status='ACTIVE',lmp_date=lmp,estimated_due_date=due,is_multiple=False,is_first_pregnancy=True,provider_status='DOCTOR')
        for week in range(1,41):
            PregnancyWeek.objects.update_or_create(week_number=week,defaults={'baby_summary':f'Demo fetal-development summary for week {week}; not medically validated content.','mother_summary':f'Demo maternal-body summary for week {week}; individual experiences vary.','baby_size_text':'Demo size not recorded' if week!=24 else 'About 30 cm — demo only','baby_weight_text':'Demo weight not recorded' if week!=24 else 'About 600 g — demo only','nutrition_summary':'General demo nutrition content; seek professional guidance for personal recommendations.','activity_summary':'General non-diagnostic demo activity content.','care_summary':'Review recorded care tasks, measurements, and upcoming events.','attention_summary':'If a symptom is severe, sudden, worsening, or concerning, contact a doctor, midwife, or appropriate healthcare facility for assessment.','medical_reviewer':'','source_information':'Demo content — source not added.'})
        # 120 templates and user tasks (3 per week)
        for week in range(1,41):
            scheduled=lmp+timedelta(days=(week-1)*7)
            for idx,(title,category) in enumerate([('Record a measurement','MEASUREMENT'),('Review this week information','LEARNING'),('Review upcoming care','PLANNING')]):
                t,_=CareTaskTemplate.objects.update_or_create(title=f'{title} — week {week}',week_from=week,week_to=week,defaults={'description':'Demo care task used to exercise software behavior; not a medical prescription.','category':category,'is_active':True,'sort_order':idx})
                UserCareTask.objects.update_or_create(pregnancy=p,template=t,scheduled_date=scheduled,defaults={'status':'COMPLETED' if week<24 else 'PENDING','completed_at':now if week<24 else None})
        weights=[63.0,63.4,63.7,64.1,64.5,64.9,65.3,65.8,66.2,66.6,67.0,67.4]
        for i,v in enumerate(weights): WeightMeasurement.objects.create(pregnancy=p,value_kg=Decimal(str(v)),measured_at=now-timedelta(weeks=len(weights)-1-i),note='Demo measurement')
        bps=[(108,69),(110,70),(111,71),(109,70),(112,72),(110,71),(113,72),(111,70),(112,71),(112,72)]
        for i,(s,d) in enumerate(bps): BloodPressureMeasurement.objects.create(pregnancy=p,systolic=s,diastolic=d,pulse=76+i%4,measured_at=now-timedelta(days=(len(bps)-1-i)*4),note='')
        gs=[88,94,101,90,97,105,91,92];types=['FASTING','BEFORE_MEAL','AFTER_MEAL','OTHER']
        for i,v in enumerate(gs): BloodGlucoseMeasurement.objects.create(pregnancy=p,value=Decimal(v),measurement_type=types[i%4],measured_at=now-timedelta(days=(len(gs)-1-i)*5),note='')
        symptom_types=['FATIGUE','BACK_PAIN','HEARTBURN','LEG_CRAMPS','SLEEP_CHANGES','NAUSEA','HEADACHE','FREQUENT_URINATION','MOOD_CHANGES','BACK_PAIN','FATIGUE','HEARTBURN','LEG_CRAMPS','FATIGUE','BACK_PAIN']
        for i,t in enumerate(symptom_types): SymptomEntry.objects.create(pregnancy=p,symptom_type=t,severity=['MILD','MODERATE','MILD'][i%3],occurred_at=now-timedelta(days=0 if i>=13 else 14-i),note='Demo symptom record')
        visits=[(-56,'COMPLETED','Demo doctor'),(-28,'COMPLETED','Demo midwife'),(3,'UPCOMING','Demo specialist'),(28,'UPCOMING','Demo follow-up')]
        created=[]
        for days,status,name in visits: created.append(PrenatalVisit.objects.create(pregnancy=p,provider_name=name,provider_type='MIDWIFE' if 'midwife' in name.lower() else 'DOCTOR',clinic_name='Demo clinic',scheduled_at=now+timedelta(days=days),status=status,notes='Demo visit record'))
        VisitQuestion.objects.create(visit=created[2],question='Is my recorded weight trend appropriate for me?');VisitQuestion.objects.create(visit=created[2],question='What should I discuss about my recorded leg cramps?')
        labs=[('CBC',-112,'COMPLETED'),('Urinalysis',-91,'COMPLETED'),('Blood Sugar',-70,'COMPLETED'),('TSH',-56,'COMPLETED'),('Demo follow-up lab',-21,'COMPLETED'),('CBC',6,'SCHEDULED'),('Demo follow-up test',35,'SCHEDULED')]
        for title,days,status in labs: LabRecord.objects.create(pregnancy=p,title=title,performed_at=now+timedelta(days=days),status=status,result_summary='Demo result summary; not medical interpretation.' if status=='COMPLETED' else '',notes='')
        for idx,(days,week) in enumerate([(-105,9),(-70,14),(-28,20),(24,27)],1): UltrasoundRecord.objects.create(pregnancy=p,title=f'Demo ultrasound {idx}',performed_at=now+timedelta(days=days),gestational_week=week,center_name='Demo imaging center',summary='Demo summary; no medical interpretation.' if days<0 else '')
        meds=[('Folic Acid',-150,True),('Vitamin D',-120,True),('Iron',-60,True),('Demo supplement',-42,True),('Historical medication',-120,False)]
        for name,days,active in meds: Medication.objects.create(pregnancy=p,name=name,dosage_text='As recorded by user — demo',schedule_text='Recorded schedule — demo',start_date=today+timedelta(days=days),end_date=None if active else today-timedelta(days=60),notes='The app does not prescribe, start, stop, or change medication.',is_active=active)
        codes=[('PREGNANCY','Pregnancy'),('NUTRITION','Nutrition'),('MATERNAL_HEALTH','Maternal Health'),('TESTS','Tests'),('BIRTH_PREPARATION','Birth Preparation'),('MENTAL_HEALTH','Mental Health')]
        categories=[]
        for i,(code,title) in enumerate(codes): categories.append(ArticleCategory.objects.update_or_create(code=code,defaults={'title':title,'sort_order':i})[0])
        for i in range(1,26):
            wf=min(i*2,24) if i<=10 else None;wt=min((wf or 0)+4,40) if wf else None
            Article.objects.update_or_create(slug=f'demo-article-{i}',defaults={'title':'Demo week 24 care article' if i==1 else f'Demo educational article {i}','summary':'Demo-only educational summary for UI/API testing.','body':'This is structured demo content. It is supportive/educational and does not replace medical advice from a doctor or midwife.\n\nSource not recorded in the demo version.','category':categories[(i-1)%len(categories)],'reading_time':3+i%5,'week_from':24 if i==1 else wf,'week_to':24 if i==1 else wt,'medical_reviewer':'','last_medically_reviewed_at':None,'source_notes':'Demo content — source not added.','is_published':True,'published_at':now-timedelta(days=i)})
        # A small set of source-backed reference articles for local product testing.
        # These are educational summaries of public guidance, not patient-specific advice.
        reference_articles = [
            {
                'slug': 'reference-antenatal-care-who',
                'title': 'مراقبت دوران بارداری و تماس منظم با مراقب سلامت',
                'summary': 'خلاصه آموزشی مبتنی بر راهنمای عمومی WHO درباره اهمیت مراقبت منظم دوران بارداری و مراقبت فردمحور.',
                'body': 'مراقبت دوران بارداری بستری برای ارتقای سلامت، ارزیابی مادر و جنین، پیشگیری و شناسایی به‌موقع مشکلات است. این متن فقط خلاصه آموزشی برای تست محصول است و جایگزین توصیه پزشک یا ماما نیست.',
                'category': categories[2],
                'reading_time': 4,
                'week_from': None,
                'week_to': None,
                'source_notes': 'WHO — Recommendations on antenatal care for a positive pregnancy experience: https://www.who.int/publications/i/item/9789241549912',
            },
            {
                'slug': 'reference-antenatal-contacts-who',
                'title': 'پیگیری منظم مراقبت بارداری',
                'summary': 'محتوای مرجع برای نمایش اهمیت تماس منظم با مراقبان سلامت در دوران بارداری.',
                'body': 'WHO مراقبت منظم دوران بارداری را یکی از اجزای اصلی مراقبت مادر می‌داند. زمان‌بندی و تعداد ویزیت‌ها باید با سیستم سلامت محل زندگی و وضعیت فردی هماهنگ شود. این محتوا تشخیصی یا تجویزی نیست.',
                'category': categories[0],
                'reading_time': 3,
                'week_from': None,
                'week_to': None,
                'source_notes': 'WHO — Promoting healthy pregnancy: https://www.who.int/health-topics/infant-nutrition/promoting-healthy-pregnancy',
            },
            {
                'slug': 'reference-week-24-nhs',
                'title': 'هفته ۲۴ بارداری — محتوای مرجع عمومی',
                'summary': 'خلاصه‌ای کوتاه برای تست نمایش محتوای هفته ۲۴، مبتنی بر راهنمای عمومی NHS.',
                'body': 'در حوالی هفته ۲۴، تغییرات بدن و رشد جنین ادامه دارد و تجربه افراد می‌تواند متفاوت باشد. برای تصمیم‌های مربوط به واکسیناسیون، علائم یا مراقبت شخصی با پزشک یا ماما هماهنگ کنید. این متن نسخه‌ی خلاصه و آموزشی است.',
                'category': categories[0],
                'reading_time': 4,
                'week_from': 24,
                'week_to': 24,
                'source_notes': 'NHS — 24 weeks pregnant guide: https://www.nhs.uk/best-start-in-life/pregnancy/week-by-week-guide-to-pregnancy/2nd-trimester/week-24/',
            },
        ]
        for item in reference_articles:
            Article.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title'],
                    'summary': item['summary'],
                    'body': item['body'],
                    'category': item['category'],
                    'reading_time': item['reading_time'],
                    'week_from': item['week_from'],
                    'week_to': item['week_to'],
                    'medical_reviewer': '',
                    'last_medically_reviewed_at': None,
                    'source_notes': item['source_notes'],
                    'is_published': True,
                    'published_at': now,
                },
            )

        reminder_types=['VISIT','LAB','ULTRASOUND','MEDICATION','MEASUREMENT','PERSONAL']
        for i in range(15): Reminder.objects.create(user=user,pregnancy=p,title=f'Demo reminder {i+1}',type=reminder_types[i%6],scheduled_at=now+timedelta(days=i-4),is_completed=i<4,note='Demo reminder note' if i%4==0 else '')
        self.stdout.write(self.style.SUCCESS(f'Seeded demo user 09120000000 and active pregnancy {p.id}. DEBUG OTP is 123456.'))
