# some_app/views.py
from django.views.generic import TemplateView, DetailView,CreateView
from .models import Document
from subscription.models import Download, PageView
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django_json_ld.views import JsonLdDetailView
from django.views import View
from django.shortcuts import render
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from meta.views import Meta
from django_json_ld.views import JsonLdContextMixin,settings,JsonLdSingleObjectMixin
from django.utils.translation import gettext as _
from haystack.generic_views import SearchMixin, SearchView
from meta.views import MetadataMixin
from django.views.generic.list import ListView
from post_office import mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files.base import ContentFile
import logging
logger = logging.getLogger(__name__)


class DocumentView(JsonLdDetailView):
    model = Document

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = self.get_object()
        entry = Document.objects.get(slug=slug)
        mlt = SearchQuerySet().more_like_this(entry)
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
        context['more'] = mlt
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            document_obj = Document.objects.get(slug=slug)
            download_obj = Download.objects.create(user=request.user, document=document_obj)
            # to-do
            attachments = {}
            pdf_doc_name = document_obj.pdf_converted_file.name.split('/')[-1]
            attachments[pdf_doc_name] = ContentFile(document_obj.pdf_converted_file.file.read())
            self.object = self.get_object()
            mlt = SearchQuerySet().more_like_this(download_obj)

            mail.send(
                request.user.email,  # List of email addresses also accepted
                settings.DEFAULT_FROM_EMAIL,
                subject='Your Download',
                message='Hi there!',
                html_message='Hi <strong>Here is your download</strong>!',
                attachments= attachments,
                priority= 'now'
            )

            logger.info("mail send")
            context = self.get_context_data(object=self.object)
            context['more'] = mlt

            return render(request, 'documents/document_detail.html',context)
        except Exception as e:
            print(e)





        # download_add = Download.objects.create(document , user)

        # return render(request, 'documents/document_detail.html')

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context




