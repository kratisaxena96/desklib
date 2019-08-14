from documents.models import Document, Report
from rest_framework import serializers


class DocumentFeedbackSerializer(serializers.Serializer):
    helpful = serializers.BooleanField(required=False)

    # class Meta:
    #     model = Document
    #     fields = ['helpful']


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
