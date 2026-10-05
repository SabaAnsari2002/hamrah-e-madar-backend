from django.utils import timezone
from rest_framework import serializers
from .models import *
class VisitQuestionSerializer(serializers.ModelSerializer):
    class Meta:model=VisitQuestion;fields=['id','visit','question','is_answered','answer_note','created_at','updated_at'];read_only_fields=['id','visit','created_at','updated_at']
class PrenatalVisitSerializer(serializers.ModelSerializer):
    questions=VisitQuestionSerializer(many=True,read_only=True)
    class Meta:model=PrenatalVisit;fields=['id','pregnancy','provider_name','provider_type','clinic_name','scheduled_at','status','notes','questions','created_at','updated_at'];read_only_fields=['id','created_at','updated_at']
class LabRecordSerializer(serializers.ModelSerializer):
    attachment_available=serializers.SerializerMethodField()
    class Meta:model=LabRecord;fields=['id','pregnancy','title','performed_at','status','result_summary','notes','attachment','attachment_available','created_at','updated_at'];extra_kwargs={'attachment':{'write_only':True,'required':False}};read_only_fields=['id','created_at','updated_at']
    def get_attachment_available(self,o):return bool(o.attachment)
class UltrasoundRecordSerializer(serializers.ModelSerializer):
    attachment_available=serializers.SerializerMethodField()
    class Meta:model=UltrasoundRecord;fields=['id','pregnancy','title','performed_at','gestational_week','center_name','summary','notes','attachment','attachment_available','created_at','updated_at'];extra_kwargs={'attachment':{'write_only':True,'required':False}};read_only_fields=['id','created_at','updated_at']
    def get_attachment_available(self,o):return bool(o.attachment)
class MedicationSerializer(serializers.ModelSerializer):
    taken_today=serializers.SerializerMethodField()
    class Meta:model=Medication;fields=['id','pregnancy','name','dosage_text','schedule_text','start_date','end_date','notes','is_active','taken_today','created_at','updated_at'];read_only_fields=['id','created_at','updated_at','taken_today']
    def get_taken_today(self,o):return o.intakes.filter(date=timezone.localdate(),completed=True).exists()
