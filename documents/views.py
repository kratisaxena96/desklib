# some_app/views.py
from django.views.generic import TemplateView, DetailView,CreateView
from .models import Document
from subscription.models import Download, PageView
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django_json_ld.views import JsonLdDetailView
from django.views import View
from django.shortcuts import render
from django.urls import reverse

import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from meta.views import Meta
from django_json_ld.views import JsonLdContextMixin,settings,JsonLdSingleObjectMixin
from django.utils.translation import gettext as _
from haystack.generic_views import SearchMixin, SearchView
from meta.views import MetadataMixin
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from post_office import mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.core.files.base import ContentFile
from documents.serializers import ReportDocumentSerializer, DocumentFeedbackSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect

import logging
logger = logging.getLogger(__name__)
from django.db.models import F

class DocumentView(JsonLdDetailView):
    model = Document

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = self.get_object()
        entry = Document.objects.get(slug=slug)
        Document.objects.filter(pk=entry.pk).update(views=F('views') + 1)
        if request.user.is_anonymous:
            page_views = request.session.get('page_views')
            if page_views:
                if slug not in page_views:
                    page_views.append(slug)
                    request.session['page_views'] = page_views
                    # page_views.append(slug)
                    # print(page_views)
                else:
                    pass
            else:
                request.session['page_views']= [slug]

        else:
            PageView.objects.create(user=request.user, document=self.object)


        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    # def post(self, request, *args, **kwargs):
    #     slug = kwargs.get('slug')
    #     try:
    #         document_obj = Document.objects.get(slug=slug)
    #         download_obj = Download.objects.create(user=request.user, document=document_obj)
    #         # to-do
    #         attachments = {}
    #         pdf_doc_name = document_obj.pdf_converted_file.name.split('/')[-1]
    #         attachments[pdf_doc_name] = ContentFile(document_obj.pdf_converted_file.file.read())
    #         self.object = self.get_object()
    #         mlt = SearchQuerySet().more_like_this(download_obj)
    #
    #         mail.send(
    #             request.user.email,  # List of email addresses also accepted
    #             settings.DEFAULT_FROM_EMAIL,
    #             subject='Your Download',
    #             message='Hi there!',
    #             html_message='Hi <strong>Here is your download</strong>!',
    #             attachments= attachments,
    #             priority= 'now'
    #         )
    #
    #         logger.info("mail send")
    #         context = self.get_context_data(object=self.object)
    #         context['more'] = mlt
    #
    #         return render(request, 'documents/document_detail.html',context)
    #     except Exception as e:
    #         print(e)
    #
    #     # download_add = Download.objects.create(document , user)
    #
    #     return render(request, 'documents/document_detail.html')

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        slug = self.kwargs['slug']
        entry = Document.objects.get(slug=slug)
        mlt = SearchQuerySet().more_like_this(entry)
        context['more_like_this'] = mlt
        context['views'] = entry.views
        # start_page = self.object.preview_from
        # end_page = self.object.preview_to

        context['controlled_pages'] = self.object.pages.filter(document=self.object,no__gte=self.object.preview_from,no__lte=self.object.preview_to)

        return context

    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.request.user.is_anonymous:
            self.template_name = 'documents/document_detail.html'
        elif hasattr(self.request.user, 'subscription'):
            self.template_name = 'documents/document_detail_subscribed.html'
        else:
            self.template_name = 'documents/document_detail_logged_in.html'

        return [self.template_name]

class DocumentDownloadView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/download_success_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.subscriptions.all().exists():
            slug = kwargs.get('slug')
            try:
                document_obj = Document.objects.get(slug=slug)
                download_obj = Download.objects.create(user=request.user, document=document_obj)
                attachments = {}
                pdf_doc_name = document_obj.pdf_converted_file.name.split('/')[-1]
                attachments[pdf_doc_name] = ContentFile(document_obj.pdf_converted_file.file.read())

                mail.send(
                    request.user.email,  # List of email addresses also accepted
                    settings.DEFAULT_FROM_EMAIL,
                    subject='Your Download',
                    message='Hi there!',
                    html_message='Hi <strong>Here is your download</strong>!',
                    attachments=attachments,
                    priority='now'
                )

                logger.info("mail send")

            except Exception as e:
                print(e)
            return render(request, 'documents/download_success_page.html')
        else:
            return HttpResponseRedirect(reverse('payment'))


class ReportDocumentApi(CreateAPIView):
    serializer_class = ReportDocumentSerializer

    def create(self, request, *args, **kwargs):
        # profile = get_object_or_404(ScheduleCall, pk=pk)
        # serializer = ScheduleCallSerializer(data=request.data)
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
        #             inquirer_ph_no = serializer.validated_data['inquirer_ph_no']
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




