from rest_framework.generics import CreateAPIView, GenericAPIView
from homework_help.serializers import CommentCreateSerializer
from desklib.mixins import RestrictIpMixin
from rest_framework.response import Response
from rest_framework import status


class CommentCreateApiView(RestrictIpMixin, CreateAPIView):
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({'serializer': serializer})
        print(serializer.validated_data['package'])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

