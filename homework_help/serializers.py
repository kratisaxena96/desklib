from rest_framework import serializers
from homework_help.models import Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    reference_files = serializers.FileField(required=False)
    message = serializers.CharField()

    class Meta:
        model = Comment
        fields = ('message', 'reference_files')
