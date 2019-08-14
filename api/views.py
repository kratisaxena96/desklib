from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from api.serializers import DocumentCreateSerializer

class DocumentCreateApiView(CreateAPIView):
    serializer_class = DocumentCreateSerializer






# Create your views here.
