from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from documents.models import Document
from documents.models import Report
from uploads.models import Upload, UploadForDocument
from django_countries.serializer_fields import CountryField


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


class UploadDocumentSerializer(serializers.ModelSerializer):
    # author = serializers.CharField(required=False)
    upload_file = serializers.FileField(required=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    # required_document = serializers.CharField(required=False)
    course_code = serializers.CharField(required=False)
    country = CountryField(required= False)
    university = serializers.CharField(required=False)

    class Meta:
        model = Upload
        fields = ['course_code', 'country', 'university', 'upload_file', 'unique_id', 'course_name', 'subjects', 'type']


class UploadForDocumentSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(required=False)
    required_document = serializers.CharField(required=False)

    class Meta:
        model = UploadForDocument
        fields = ('required_document', 'uid')
