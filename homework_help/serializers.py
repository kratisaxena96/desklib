from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from homework_help.models import Comment, Question, QuestionFile, Order, Answers


class QuestionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('question', 'subjects')


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('question', 'uuid')


class QuestionFileCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])])

    class Meta:
        model = QuestionFile
        fields = ('file', 'unique_id')


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


class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('status', 'budget')


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = ('solution', 'solution_files')
