from rest_framework import serializers
from documents.models import Document
from documents.models import Report


class DocumentCreateSerializer(serializers.ModelSerializer):
    upload_file = serializers.FileField()
    # classifier =

    class Meta:
        model = Document
        fields = ('upload_file', 'is_published', 'is_visible',)


class DocumentFeedbackSerializer(serializers.Serializer):
    helpful = serializers.BooleanField(required=False)


class ReportDocumentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(required=False)
    issue = serializers.CharField(required=True)
    other_issue = serializers.CharField(required=False)

    class Meta:
        model = Report
        fields = ['issue', 'other_issue', 'document', 'author']
