from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from homework_help.models import Comment, Question


class QuestionCreateSerializer(serializers.ModelSerializer):
    upload_file = serializers.FileField()

    class Meta:
        model = Question
        fields = ('question', 'upload_file', 'subjects')


class CommentCreateSerializer(serializers.ModelSerializer):
    reference_files = serializers.FileField(required=False, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])])
    message = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = ('message', 'reference_files')

    def validate(self, data):
        reference_files = data.get('reference_files')
        message = data.get('message')

        if not reference_files and not message:
            raise serializers.ValidationError("Fill any one field either message or file.")

        return data
