# some_app/views.py
import logging
import os
import tempfile

logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from django.views.generic import TemplateView, DetailView,CreateView, FormView
from .models import Document
from subscription.models import Download, PageView, SessionPageView
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django_json_ld.views import JsonLdDetailView
from django.template.loader import render_to_string

from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import get_template
from django.template import Context
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
from .forms import ReportForm, DownloadFileForm

from django.db.models import F
from datetime import timedelta
from subscription.utils import is_subscribed, get_current_subscription
from django.core.files import File as DjangoFile


class DocumentView(JsonLdDetailView):
    model = Document
    form = ReportForm

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = self.get_object()
        entry = Document.objects.get(slug=slug)
        Document.objects.filter(pk=entry.pk).update(views=F('views') + 1)
        if not self.request.user.is_anonymous:
            check_subscribed_status = is_subscribed(self.request.user)
        else:
            check_subscribed_status = False

        pageviews_left = True

        if check_subscribed_status:
            subscription_obj = get_current_subscription(self.request.user)
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

            if view_limit_count < plan_view_limit:
                PageView.objects.create(user=request.user, document=self.object)
                pageviews_left = True
                # context = self.get_context_data(object=self.object)
                # return self.render_to_response(context)
            else:
                pageviews_left = False

        else:
            page_views = request.session.get('page_views')

            if page_views:
                if len(page_views) < 5:
                    pageviews_left = True
                    if slug not in page_views:
                        page_views.append(slug)
                        request.session['page_views'] = page_views
                        SessionPageView.objects.create(session=request.session.session_key, document=self.object)
                        # page_views.append(slug)
                        # print(page_views)
                    else:
                        pageviews_left = True

                        # context = self.get_context_data(object=self.object)
                        # return self.render_to_response(context)
                else:
                    pageviews_left = False
                    # context = ''
                    # return self.render_to_response(context)

            else:
                pageviews_left = True
                request.session['page_views'] = [slug]
                SessionPageView.objects.create(session=request.session.session_key, document=self.object)
                # context = self.get_context_data(object=self.object)
                # return self.render_to_response(context)

        context = self.get_context_data(object=self.object)
        context['pageviews_flag'] = pageviews_left

        return self.render_to_response(context)

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
        elif is_subscribed(self.request.user):
            self.template_name = 'documents/document_detail_subscribed.html'
        else:
            self.template_name = 'documents/document_detail_logged_in.html'

        return [self.template_name]


# class DocumentDownloadView(LoginRequiredMixin, TemplateView):
#
#     def get(self, request, *args, **kwargs):
#         # print(request.user)
#         if request.user.subscriptions.all().exists():
#             check_subscribed_status = is_subscribed(self.request.user)
#
#             if check_subscribed_status:
#                 subscription_obj = get_current_subscription(self.request.user)
#                 expiry_date_subscription = subscription_obj.expire_on
#                 plan = subscription_obj.plan
#                 plan_days = plan.days
#                 plan_download_limit = plan.download_limit
#                 startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
#                 download_count = Download.objects.filter(user=self.request.user, created_at__gte=startdate_subscription,
#                                                          created_at__lte=expiry_date_subscription).count()
#                 remaining_downloads = plan_download_limit - download_count
#
#                 if remaining_downloads > 0 :
#                     slug = kwargs.get('slug')
#                     try:
#                         document_obj = Document.objects.get(slug=slug)
#                         Download.objects.create(user=request.user, document=document_obj)
#                         Document.objects.filter(pk=document_obj.pk).update(total_downloads=F('total_downloads') + 1)
#                         attachments = {}
#                         pdf_doc_name = document_obj.pdf_converted_file.name.split('/')[-1]
#                         attachments[pdf_doc_name] = ContentFile(document_obj.pdf_converted_file.file.read())
#
#                         mail.send(
#                             request.user.email,  # List of email addresses also accepted
#                             settings.DEFAULT_FROM_EMAIL,
#                             subject='Your Download',
#                             message='Hi there!',
#                             html_message='Hi <strong>Here is your download</strong>!',
#                             attachments=attachments,
#                             priority='now'
#                         )
#
#                         logger.info("mail send")
#
#                     except Exception as e:
#                         print(e)
#
#
#             return redirect('documents:download-success-view')
#         else:
#             return redirect('subscription')


class DocumentDownloadDetailView(LoginRequiredMixin, FormView):
    template_name = 'documents/download_info.html'
    form_class = DownloadFileForm

    def get_context_data(self, **kwargs):
        context = super(DocumentDownloadDetailView, self).get_context_data(**kwargs)
        subscription_obj = get_current_subscription(self.request.user)
        expiry_date_subscription = subscription_obj.expire_on
        plan = subscription_obj.plan
        plan_days = plan.days
        plan_download_limit = plan.download_limit
        startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
        download_count = Download.objects.filter(user=self.request.user, created_at__gte=startdate_subscription,
                                                 created_at__lte=expiry_date_subscription).count()
        remaining_downloads = plan_download_limit - download_count
        document_obj = Document.objects.get(slug=self.kwargs.get('slug'))
        from haystack.inputs import Raw
        # sqs = SearchQuerySet().filter(content= self.kwargs.get('slug'))
        # searchqueryset = SearchQuerySet().filter(slug=self.kwargs.get('slug'))
        # SearchIndex.get_model(self)
        if document_obj.cover_page_number:
            context['image'] =  document_obj.pages.get(no=document_obj.cover_page_number).image_file
        else:
            context['image'] = document_obj.pages.first().image_file
        context['remaining_downloads'] = remaining_downloads
        context['document'] = document_obj
        context['subscription'] = subscription_obj
        return context

    def post(self, request, *args, **kwargs):

        form = DownloadFileForm(self.request.POST)
        # print(request.user)
        if form.is_valid():

            # Generating filename without spaces. Replacing them with underscore.
            filename = Document.objects.get(slug=kwargs.get('slug')).upload_file.name
            filename = os.path.basename(filename)
            filename = filename.replace(' ', '_')

            f1 = Document.objects.get(slug=kwargs.get('slug')).upload_file.file  # File to copy from
            temp = tempfile.NamedTemporaryFile(suffix=filename)  # Temporary File to copy to

            with open(temp.name, 'wb') as f2:
                f2.write(f1.read())

            f2.close()

            pre, ext = os.path.splitext(filename)
            temp_dir = tempfile.TemporaryDirectory(prefix=pre)

            # convert the uploaded file to pdf file and save it
            os.system('soffice --headless --convert-to pdf --outdir ' + temp_dir.name + ' ' + temp.name)

            pre, ext = os.path.splitext(filename)
            file_with_pdf_ext = pre + ".pdf"
            # Changing file extension
            # https://stackoverflow.com/questions/2900035/changing-file-extension-in-python
            head, tail = os.path.split(temp.name)
            pre, ext = os.path.splitext(tail)
            pdf_converted_loc = os.path.join(temp_dir.name, pre + ".pdf")

            # Reading generated pdf document from soffice and adding it to our model field
            f = open(pdf_converted_loc, 'rb')
            myfile = DjangoFile(f)  # Converting to django's File model object
            # self.pdf_converted_file = myfile
            # self.pdf_converted_file.name = file_with_pdf_ext

            subscription_obj = get_current_subscription(self.request.user)
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
                    Download.objects.create(user=request.user, document=document_obj)
                    Document.objects.filter(pk=document_obj.pk).update(total_downloads=F('total_downloads') + 1)
                    attachments = {}
                    pdf_doc_name = myfile.name.split('/')[-1]
                    attachments[pdf_doc_name] = ContentFile(myfile.file.read())

                    context = {'document': document_obj}
                    htmly = render_to_string('desklib/mail-templates/document_download_email.html', context,
                                             request=request)
                    # d = Context({'username':username})
                    #
                    # subject, from_email, to = 'Your Download', settings.DEFAULT_FROM_EMAIL, "rishidutta92@gmail.com"
                    # # # text_content = plaintext.render(d)
                    # # # html_content = htmly.render(html)
                    # msg = EmailMultiAlternatives(subject, "TEXTCONTENT", from_email, [to])
                    # msg.attach_alternative(htmly, "text/html")
                    # res = msg.send()
                    #
                    mail.send(
                        request.user.email,  # List of email addresses also accepted
                        settings.DEFAULT_FROM_EMAIL,
                        subject='Your Downloaded Document From Desklib',
                        # message=htmly,
                        html_message=htmly,
                        attachments=attachments,
                        priority='now'
                    )
                    # mail.send(
                    #     request.user.email,  # List of email addresses also accepted
                    #     settings.DEFAULT_FROM_EMAIL,
                    #     subject='Your Download',
                    #     message='Hi there!',
                    #     html_message='Hi <strong>Here is your download</strong>!',
                    #     attachments=attachments,
                    #     priority='now'
                    # )

                    logger.info("mail send")

                except Exception as e:
                    print(e)
            return redirect('documents:download-success-view')
        else:
            return render(request, self.template_name, {
                'form': form,
            })



class DocumentDownloadView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        # print(request.user)
        if request.user.subscriptions.all().exists():
            subscription_obj = get_current_subscription(self.request.user)
            if subscription_obj:
                return redirect('documents:download-info-view', slug=kwargs.get('slug'))
            else:
                return redirect('subscription')
        else:
            return redirect('subscription')


class DownloadSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/download_success.html'

    def get_context_data(self, **kwargs):
        context = super(DownloadSuccessView, self).get_context_data(**kwargs)
        try:
            remaining_downloads_flag = False
            subscription_obj = get_current_subscription(self.request.user)
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






