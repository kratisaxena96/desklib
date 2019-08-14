from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from django.conf import settings
from post_office import mail
from documents.models import Document
from api.serializers import DocumentCreateSerializer, CreateSampleSerializer, ReportDocumentSerializer, DocumentFeedbackSerializer

class DocumentCreateApiView(CreateAPIView):
    serializer_class = DocumentCreateSerializer


class CreateSampleApiView(CreateAPIView):
    serializer_class = CreateSampleSerializer


class ReportDocumentApi(CreateAPIView):
    serializer_class = ReportDocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'serializer': serializer})

        serializer.validated_data['author'] = self.request.user
        reported_by = serializer.validated_data['author']
        reported_document = serializer.validated_data['document']
        reported_issue = serializer.validated_data['issue']
        if not reported_issue:
            reported_issue = serializer.validated_data['other_issue']

        locus_email = "kushagra.goel@locusrags.com"
        if not settings.DEBUG:
            locus_email = "locus@locus.com"

        mail.send(
            locus_email,  # List of email addresses also accepted
            #                 'from@example.com',
            subject='{{reported_document|safe}} reported',
            message='{{reported_document|safe}} reported!',
            html_message='{{reported_document|safe}} is reported by {{reported_by}}.<br>Issue is {{reported_issue}}',
            context={'reported_document': reported_document, 'reported_issue': reported_issue, 'reported_by': reported_by},
            priority='now',
        )
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DocumentFeedbackApi(GenericAPIView):
    serializer_class = DocumentFeedbackSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'serializer': serializer})
        # document = Document.objects.get(title=serializer.validated_data['title']).was_helpful
        document = Document.objects.get(slug=kwargs['slug'])
        helpful = serializer.validated_data['helpful']
        if helpful == True:
            document.was_helpful = document.was_helpful + 1
        else:
            document.not_helpful = document.not_helpful + 1

        document.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

# Create your views here.
