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
    class Meta:
        model = Report
        fields = ['issue', 'other_issue', 'document', 'author']

    def validate(self, data):
        issue = data.get('issue')
        other_issue = data.get('other_issue')

        if not issue and not other_issue:
            raise serializers.ValidationError("Issue can not be blank")

        return data
