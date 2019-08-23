# some_app/views.py
import logging
logger = logging.getLogger(__name__)

from rest_framework.views import APIView

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
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.renderers import (
    HTMLFormRenderer,
    JSONRenderer,
    BrowsableAPIRenderer,
)
from .forms import reportForm

from django.db.models import F
from datetime import timedelta

class DocumentView(JsonLdDetailView):
    model = Document
    form = reportForm

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = self.get_object()
        entry = Document.objects.get(slug=slug)
        Document.objects.filter(pk=entry.pk).update(views=F('views') + 1)
        if request.user.is_anonymous:
            page_views = request.session.get('page_views')
            if page_views:
                if len(page_views) < 5:
                    print(page_views)
                    if slug not in page_views:
                        page_views.append(slug)
                        request.session['page_views'] = page_views
                        # page_views.append(slug)
                        # print(page_views)
                    else:
                        pass
                else:
                    return redirect('documents:pageviews-finish-view')
            else:
                request.session['page_views'] = [slug]
        else:
            subscription_obj = self.request.user.subscriptions.all().get(is_current=True)
            if subscription_obj:
                expiry_date_subscription = subscription_obj.expire_on
                plan = subscription_obj.plan
                plan_days = plan.days
                plan_view_limit = plan.view_limit
                startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
                view_limit_count = PageView.objects.filter(user=self.request.user,
                                                         created_at__gte=startdate_subscription,
                                                         created_at__lte=expiry_date_subscription).count()
                # remaining_page_view = plan_view_limit - view_limit_count
                # print(remaining_page_view)

                if view_limit_count <= plan_view_limit:
                    PageView.objects.create(user=request.user, document=self.object)
                    context = self.get_context_data(object=self.object)
                    return self.render_to_response(context)
                else:
                    return redirect('documents:pageviews-finish-view')





    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        slug = self.kwargs['slug']
        entry = Document.objects.get(slug=slug)
        subjects = entry.subjects.all()
        # mlt = SearchQuerySet().more_like_this(entry)[:6]
        if subjects:
            s = "context['more_like_this'] = SearchQuerySet()"
            for sub in subjects:
              s += ".filter_or(subjects='"+str(sub)+"',)"
            s +="[:6]"
            exec(s)
        # else:
        #     context['more_like_this'] = SearchQuerySet().more_like_this(entry)[:6]

        # context['more_like_this'] = SearchQuerySet().filter_or(subjects='artificial-intelligence',).filter_or(subjects='engineering')
        context['views'] = entry.views
        context['form'] = self.form
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
        elif self.request.user.subscriptions.all().filter(is_current = True):
            self.template_name = 'documents/document_detail_subscribed.html'
        else:
            self.template_name = 'documents/document_detail_logged_in.html'

        return [self.template_name]

class DocumentDownloadView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        print(request.user)
        if request.user.subscriptions.all().exists():
            subscription_obj = self.request.user.subscriptions.all().get(is_current=True)
            if subscription_obj:
                expiry_date_subscription = subscription_obj.expire_on
                plan = subscription_obj.plan
                plan_days = plan.days
                plan_download_limit = plan.download_limit
                startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
                download_count = Download.objects.filter(user=self.request.user, created_at__gte=startdate_subscription,
                                                         created_at__lte=expiry_date_subscription).count()
                remaining_downloads = plan_download_limit - download_count

                if remaining_downloads > 0 :
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


            return redirect('documents:download-success-view')
        else:
            return redirect('subscription')

class DownloadSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/download_success_page.html'

    def get_context_data(self, **kwargs):
        context = super(DownloadSuccessView, self).get_context_data(**kwargs)
        try:
            remaining_downloads_flag = False
            subscription_obj = self.request.user.subscriptions.all().get(is_current=True)
            expiry_date_subscription = subscription_obj.expire_on
            plan = subscription_obj.plan
            plan_days = plan.days
            plan_download_limit = plan.download_limit
            startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
            download_count = Download.objects.filter(user=self.request.user, created_at__gte=startdate_subscription,
                                                     created_at__lte=expiry_date_subscription).count()
            remaining_downloads = plan_download_limit - download_count
            context['remaining_downloads'] = remaining_downloads


            if remaining_downloads < 0:
                remaining_downloads_flag = False
            else:
                remaining_downloads_flag = True

            context['remaining_downloads_flag'] = remaining_downloads_flag


        except Exception as e:
            print(e)

        return context

class PageViewsFinishView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/page_views_finish.html'






