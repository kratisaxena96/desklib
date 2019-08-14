from rest_framework import serializers
from documents.models import Document


class DocumentCreateSerializer(serializers.Serializer):
    upload_file = serializers.FileField()
    helpful = serializers.BooleanField()

    # class Meta:
        # model = Document
        # fields = ('upload_file',)
