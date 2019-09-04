from rest_framework import serializers
from samples.models import Sample


class CreateSampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sample
        fields = ['name','author','upload_sample','seo_title','seo_description','seo_keywords']



