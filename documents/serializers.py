from documents.models import Document, Report
from rest_framework import serializers


class DocumentFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['was_heplful', 'not_heplful', 'title']


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
