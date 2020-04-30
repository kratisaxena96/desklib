from rest_framework.generics import CreateAPIView
from contact.serializers import QueryCreateSerializer
from rest_framework.response import Response
from rest_framework import status


class QueryCreateApiView(CreateAPIView):
    serializer_class = QueryCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)