from rest_framework import serializers
from documents.models import Document
from samples.models import Sample
from documents.models import  Report

class DocumentCreateSerializer(serializers.ModelSerializer):
    upload_file = serializers.FileField()

    class Meta:
        model = Document
        fields = ('upload_file',)


class CreateSampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = ['name','author','upload_sample','seo_title','seo_description','seo_keywords']



class DocumentFeedbackSerializer(serializers.Serializer):
    helpful = serializers.BooleanField(required=False)

class ReportDocumentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(required=False)
    issue = serializers.CharField(required=True)
    other_issue = serializers.CharField(required=False)

    class Meta:
        model = Report
        fields = ['issue', 'other_issue', 'document', 'author']
