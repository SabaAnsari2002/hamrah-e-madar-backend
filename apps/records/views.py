from django.http import FileResponse,Http404
from django.utils import timezone
from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from config.ownership import PregnancyOwnedQuerysetMixin
from apps.audit.models import AuditLog
from .models import *
from .serializers import *
from .filters import VisitFilter,LabFilter,UltrasoundFilter,MedicationFilter

class OwnedRecordViewSet(PregnancyOwnedQuerysetMixin,viewsets.ModelViewSet):
    filterset_fields=['pregnancy'];ordering_fields=['created_at'];
    def perform_create(self,serializer):
        super().perform_create(serializer);obj=serializer.instance
        if hasattr(obj,'attachment') and obj.attachment:AuditLog.objects.create(user=self.request.user,action=AuditLog.Action.FILE_UPLOAD,object_type=obj.__class__.__name__,object_id=str(obj.id))
class PrenatalVisitViewSet(OwnedRecordViewSet):
    queryset=PrenatalVisit.objects.select_related('pregnancy').prefetch_related('questions');serializer_class=PrenatalVisitSerializer;filterset_class=VisitFilter;ordering_fields=['scheduled_at','created_at'];ordering=['-scheduled_at']
    @action(detail=True,methods=['get','post'],url_path='questions')
    def questions(self,request,pk=None):
        visit=self.get_object()
        if request.method=='GET':return Response(VisitQuestionSerializer(visit.questions.all(),many=True).data)
        s=VisitQuestionSerializer(data=request.data);s.is_valid(raise_exception=True);q=s.save(visit=visit);return Response(VisitQuestionSerializer(q).data,status=201)
class LabRecordViewSet(OwnedRecordViewSet):
    queryset=LabRecord.objects.select_related('pregnancy');serializer_class=LabRecordSerializer;filterset_class=LabFilter;ordering_fields=['performed_at','created_at'];ordering=['-performed_at']
    @action(detail=True,methods=['get'],url_path='attachment')
    def attachment(self,request,pk=None):
        obj=self.get_object()
        if not obj.attachment:raise Http404
        return FileResponse(obj.attachment.open('rb'),as_attachment=True,filename=obj.attachment.name.split('/')[-1])
class UltrasoundRecordViewSet(OwnedRecordViewSet):
    queryset=UltrasoundRecord.objects.select_related('pregnancy');serializer_class=UltrasoundRecordSerializer;filterset_class=UltrasoundFilter;ordering_fields=['performed_at','created_at'];ordering=['-performed_at']
    @action(detail=True,methods=['get'],url_path='attachment')
    def attachment(self,request,pk=None):
        obj=self.get_object()
        if not obj.attachment:raise Http404
        return FileResponse(obj.attachment.open('rb'),as_attachment=True,filename=obj.attachment.name.split('/')[-1])
class MedicationViewSet(OwnedRecordViewSet):
    queryset=Medication.objects.select_related('pregnancy').prefetch_related('intakes');serializer_class=MedicationSerializer;filterset_class=MedicationFilter;ordering_fields=['start_date','created_at'];ordering=['-is_active','-start_date']
    @action(detail=True,methods=['post'],url_path='today-completion')
    def today_completion(self,request,pk=None):
        med=self.get_object();completed=bool(request.data.get('completed',True));obj,_=MedicationIntake.objects.update_or_create(medication=med,date=timezone.localdate(),defaults={'completed':completed});return Response({'medication':str(med.id),'date':obj.date,'completed':obj.completed})
class VisitQuestionDetailViewSet(viewsets.GenericViewSet):
    queryset=VisitQuestion.objects.select_related('visit__pregnancy');serializer_class=VisitQuestionSerializer
    def get_queryset(self):return super().get_queryset().filter(visit__pregnancy__user=self.request.user)
    def partial_update(self,request,pk=None):
        q=self.get_object();s=self.get_serializer(q,data=request.data,partial=True);s.is_valid(raise_exception=True);s.save();return Response(s.data)
    def destroy(self,request,pk=None):self.get_object().delete();return Response(status=204)
class RecordsSummaryView(APIView):
    def get(self,request):
        p=request.user.pregnancies.filter(status='ACTIVE').first()
        if not p:return Response({'visits':[],'labs':[],'ultrasounds':[],'medications':[]})
        return Response({'visits':PrenatalVisitSerializer(PrenatalVisit.objects.filter(pregnancy=p).prefetch_related('questions')[:5],many=True).data,'labs':LabRecordSerializer(LabRecord.objects.filter(pregnancy=p)[:5],many=True).data,'ultrasounds':UltrasoundRecordSerializer(UltrasoundRecord.objects.filter(pregnancy=p)[:5],many=True).data,'medications':MedicationSerializer(Medication.objects.filter(pregnancy=p).prefetch_related('intakes')[:10],many=True).data})
