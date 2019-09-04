from rest_framework.generics import CreateAPIView
from .serializers import CreateSampleSerializer
from desklib.mixins import RestrictIpMixin


class CreateSampleApiView(RestrictIpMixin, CreateAPIView):
    serializer_class = CreateSampleSerializer

