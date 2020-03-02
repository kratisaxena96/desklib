from rest_framework import serializers
from homework_help.models import Comment, Question


class QuestionCreateSerializer(serializers.ModelSerializer):
    upload_file = serializers.FileField()

    class Meta:
        model = Question
        fields = ('question', 'upload_file', 'subjects')


class CommentCreateSerializer(serializers.ModelSerializer):
    reference_files = serializers.FileField(required=False)
    message = serializers.CharField()

    class Meta:
        model = Comment
        fields = ('message', 'reference_files')
