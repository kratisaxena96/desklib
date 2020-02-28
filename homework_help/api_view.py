from rest_framework.generics import CreateAPIView

from homework_help.serializers import QuestionCreateSerializer


class QuestionCreateApiView(CreateAPIView):
    serializer_class = QuestionCreateSerializer
