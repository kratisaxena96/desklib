from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from django.conf import settings
from post_office import mail
from documents.models import Document
from .serializers import DocumentCreateSerializer, ReportDocumentSerializer, DocumentFeedbackSerializer, UploadDocumentSerializer, UploadForDocumentSerializer
from desklib.mixins import RestrictIpMixin
from samples.models import Sample
from uploads.models import UploadForDocument, Upload
from documents.models import Issue
from rest_framework.permissions import IsAuthenticated


class DocumentCreateApiView(RestrictIpMixin, CreateAPIView):
    serializer_class = DocumentCreateSerializer


class ReportDocumentApi(CreateAPIView):
    serializer_class = ReportDocumentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'serializer': serializer})
        if not self.request.user.is_anonymous:
            serializer.validated_data['author'] = self.request.user
        reported_by = self.request.user
        reported_document = serializer.validated_data['document']
        reported_issue = serializer.validated_data['issue']
        if not reported_issue:
            reported_issue = serializer.validated_data['other_issue']
        reported_issue = Issue.objects.get(id=reported_issue).title
        locus_email = "kushagra.goel@locusrags.com"
        if not settings.DEBUG:
            locus_email = "info@desklib.com"

        subject = reported_document.title+ ' reported'
        message = reported_document.title+ ' reported!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [locus_email],
        if self.request.user.is_anonymous:
            html_message = reported_document.title+' is reported' + '.<br>Issue is '+reported_issue
        else:
            html_message = reported_document.title+' is reported by '+ reported_by.email+'.<br>Issue is '+reported_issue
        mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        mail.attach_alternative(html_message, 'text/html')
        mail.send(True)

        # mail.send(
        #     locus_email,  # List of email addresses also accepted
        #     #                 'from@example.com',
        #     subject='{{reported_document|safe}} reported',
        #     message='{{reported_document|safe}} reported!',
        #     html_message='{{reported_document|safe}} is reported by {{reported_by}}.<br>Issue is {{reported_issue}}',
        #     context={'reported_document': reported_document.title, 'reported_issue': reported_issue, 'reported_by': reported_by},
        #     priority='now',
        # )
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
            document.save(update_fields=["was_helpful"])
        else:
            document.not_helpful = document.not_helpful + 1
            document.save(update_fields=["not_helpful"])

        document.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

# Create your views here.


class UploadDocumentApi(CreateAPIView):
    serializer_class = UploadDocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({'serializer': serializer})
        if not self.request.user.is_anonymous:
            serializer.validated_data['author'] = self.request.user
        author = self.request.user
        upload_file = serializer.validated_data['upload_file']
        # required_document = Document.objects.get(slug=serializer.validated_data['required_document'])

        # locus_email = "kushagra.goel@locusrags.com"
        # if not settings.DEBUG:
        #     locus_email = "info@desklib.com"
        #
        # subject = 'Documents Uploaded for free download'
        # message = upload_file.title+ ' reported!'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = [locus_email],
        # html_message = reported_document.title+' is reported by '+ reported_by.email+'.<br>Issue is '+reported_issue
        # mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        # mail.attach_alternative(html_message, 'text/html')
        #
        # for i in question.user_questionfiles.all():
        #
        #     mime_image = MIMEImage(i.file.read())
        #     mime_image.add_header('Content-ID', '<image>', filename=i.title)
        #     mail.attach(mime_image)
        #
        #
        #     # mail.attach_file(.path)
        # mail.attach_alternative(html_message, 'text/html')
        # mail.send(True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class UploadForDocumentApiView(CreateAPIView):
    serializer_class = UploadForDocumentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        data = request.POST.getlist('unique_id')
        doc = request.POST.get('document')
        required_document = Document.objects.get(slug=doc)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=request.user, required_document=required_document)

        doc = UploadForDocument.objects.get(uid=serializer.data.get('uid'))
        # print(q.id)
        for i in data:
            qf = Upload.objects.get(unique_id=i)
            qf.upload_for_document = doc
            qf.save()


        locus_email = ('kushadmin@mailinator.com')
        if not settings.DEBUG:
            locus_email = ('info@desklib.com', 'ankit.r@zucol.in')

        subject = 'Documents Uploaded for free download'
        message = 'Documents Uploaded for free download'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = locus_email,
        html_message = 'The documents are uploaded by '+ request.user.email+'.<br>The required document is ' + required_document.title
        mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        mail.attach_alternative(html_message, 'text/html')

        mail.attach_alternative(html_message, 'text/html')
        mail.send(True)

        # if not request.user.username:
        #     return HttpResponseRedirect(redirect_to=reverse('account_login'))

        # o = Order(question=q, author=request.user)
        # o.save()
        data = serializer.data

        headers = self.get_success_headers(serializer.data)
        # return HttpResponseRedirect(reverse('homework_help:order-detail-view', {'uuid':o.uuid}))
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

