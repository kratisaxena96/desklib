from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from contact.models import ContactUsModel


class QueryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUsModel
        fields = ('name', 'email', 'message')