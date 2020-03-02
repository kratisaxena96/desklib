from rest_framework.generics import CreateAPIView

from homework_help.serializers import QuestionCreateSerializer
from rest_framework.generics import CreateAPIView, GenericAPIView
from homework_help.serializers import CommentCreateSerializer
from desklib.mixins import RestrictIpMixin
from rest_framework.response import Response
from rest_framework import status
from homework_help.models import Order




class QuestionCreateApiView(CreateAPIView):
    serializer_class = QuestionCreateSerializer


class CommentCreateApiView(RestrictIpMixin, CreateAPIView):
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data['message'])
        order = Order.objects.get(order_id=self.kwargs['order_id'])
        serializer.save(author=request.user, order=order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


