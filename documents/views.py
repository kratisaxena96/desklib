# some_app/views.py
import logging
import os
import json
import pytz
import socket
import tempfile
import requests

from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.response import TemplateResponse
from paypal.standard.forms import PayPalPaymentsForm
import geoip2.webservice

from django.contrib.gis.geoip2 import GeoIP2

from accounts.models import UserAccount
from desklib.mixins import CheckSubscriptionMixin
from documents.admin_forms import DocumentSearchForm
from documents.mixins import SubscriptionCheckMixin
from homework_help.models import Order

logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from django.views.generic import TemplateView, DetailView, CreateView, FormView
from django.views.generic.base import RedirectView
from .models import Document
from subscription.models import Download, PageView, SessionPageView, PayPerDocument, Plan
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django_json_ld.views import JsonLdDetailView
from django.template.loader import render_to_string
from subscription.models import Subscription
from django.views import View
from django.shortcuts import render
from django.urls import reverse

from haystack.query import SearchQuerySet
from meta.views import Meta, MetadataMixin
from django_json_ld.views import JsonLdContextMixin, settings, JsonLdSingleObjectMixin

from post_office import mail
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
from datetime import timedelta, datetime
from subscription.utils import is_subscribed, get_current_subscription
from django.core.files import File as DjangoFile
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect, Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from documents.utils import merge_pdf
from django.utils import timezone
from documents.forms import UploadFileForm
from uploads.forms import UploadForm
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import DefaultStorage
from uploads.models import Upload
from formtools.wizard.forms import ManagementForm
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from subscription.models import PaypalInvoice
from documents.utils import key_generator



class DocumentView(JsonLdDetailView):
    model = Document
    form = ReportForm
    queryset = Document.objects.filter(Q(is_published=True) | Q(is_visible=True))
    payperdoc = False

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        self.object = self.get_object()
        entry = Document.objects.get(slug=slug)
        if self.object.redirect_url:
            return HttpResponsePermanentRedirect(self.object.redirect_url)
        Document.objects.filter(pk=entry.pk).update(views=F('views') + 1)
        if not self.request.user.is_anonymous:
            check_subscribed_status = is_subscribed(self.request.user)
            PageView.objects.create(user=request.user, document=self.object)
        else:
            check_subscribed_status = False

        try:
            pay_per_doc_sub = self.request.user.pay_per_download.all()
            if pay_per_doc_sub:
                if pay_per_doc_sub.filter(documents=entry, expire_on__gt=timezone.now()):
                    self.payperdoc = True
                    pageviews_left = True
        except:
            pass
        if check_subscribed_status and not self.payperdoc:
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

            if view_limit_count <= plan_view_limit:
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
        if self.payperdoc:
            pageviews_left = True
        context = self.get_context_data(object=self.object)
        context['pageviews_flag'] = pageviews_left
        context['pay_per_view'] = self.payperdoc

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        slug = self.kwargs['slug']
        entry = Document.objects.get(slug=slug)
        subjects = entry.subjects.all()
        context['canonical'] = entry.canonical_url
        from haystack.inputs import AutoQuery, Raw

        # mlt = SearchQuerySet().more_like_this(entry)[:6]
        if subjects:
            s = "context['more_like_this'] = SearchQuerySet()"
            for sub in subjects:
                s += ".filter_or(subjects='" + str(sub) + "',)"
            s += "[:6]"
            exec(s)
        # else:
        #     context['more_like_this'] = SearchQuerySet().more_like_this(entry)[:6]

        # context['more_like_this'] = SearchQuerySet().filter_or(subjects='artificial-intelligence',).filter_or(subjects='engineering')
        context['views'] = entry.views
        context['form'] = self.form
        # start_page = self.object.preview_from
        # end_page = self.object.preview_to
        if self.payperdoc:
            context['controlled_pages'] = self.object.pages.filter(document=self.object)
        else:
            context['controlled_pages'] = self.object.pages.filter(document=self.object,
                                                                   no__gte=self.object.preview_from,
                                                                   no__lte=self.object.preview_to)

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
        elif self.payperdoc:
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
    payperdoc = False


    def get(self, request, *args, **kwargs):
        subscription = get_current_subscription(self.request.user)
        try:
            doc = Document.objects.get(slug=request.GET.get('doc'))
        except:
            doc = None
        try:
            pay_per_doc = PayPerDocument.objects.get(documents=doc, expire_on__gt=timezone.now(), is_current=True, user=request.user)
        except:
            pay_per_doc = None

        if subscription or pay_per_doc:
            # return super(DocumentDownloadDetailView, self).dispatch(request, *args, **kwargs)
            return self.render_to_response(self.get_context_data())
        else:
            try:
                return HttpResponseRedirect(reverse('documents:document-pay') + "?doc=" + request.GET.get('doc'))
            except:
                return render(request, 'desklib/error_404.html', status=404)

    def get_context_data(self, **kwargs):
        context = super(DocumentDownloadDetailView, self).get_context_data(**kwargs)
        document_obj = None
        try:
            document_obj = Document.objects.get(slug=self.request.GET.get('doc'))
        except:
            document_obj = Document.objects.get(slug=self.request.GET.get('slug'))
        finally:
            if document_obj is None:
                raise Http404('"No document matches the given query.')
        try:
            pay_per_doc_sub = self.request.user.pay_per_download.all()
            pay_per_doc = pay_per_doc_sub.get(documents=document_obj, expire_on__gt=timezone.now(), is_current=True )
            if pay_per_doc:
                plan = pay_per_doc.plan
                context['subscription'] = pay_per_doc
                context['remaining_downloads'] = "Single Download Plan"
        except:
            subscription_obj = get_current_subscription(self.request.user)
            expiry_date_subscription = subscription_obj.expire_on
            plan = subscription_obj.plan
            plan_download_limit = plan.download_limit

            plan_days = plan.days
            startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
            download_count = Download.objects.filter(user=self.request.user, created_at__gte=startdate_subscription,
                                                     created_at__lte=expiry_date_subscription).count()
            remaining_downloads = plan_download_limit - download_count
            context['subscription'] = subscription_obj
            context['remaining_downloads'] = remaining_downloads
        if document_obj.cover_page_number:
            context['image'] = document_obj.pages.get(no=document_obj.cover_page_number).image_file
        else:
            context['image'] = document_obj.pages.first().image_file
        context['document'] = document_obj

        return context

    def post(self, request, *args, **kwargs):

        form = DownloadFileForm(self.request.POST)
        slug = request.POST['file']

        # print(request.user)
        if form.is_valid():

            # Generating filename without spaces. Replacing them with underscore.
            filename = Document.objects.get(slug=request.POST['file']).upload_file.name
            filename = os.path.basename(filename)
            filename = filename.replace(' ', '_')

            f1 = Document.objects.get(slug=request.POST['file']).upload_file.file  # File to copy from
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

            merge_pdf(input_pdf=pdf_converted_loc,
                      output=pdf_converted_loc,
                      watermark='desklib/static/pdf/watermark-desklib.pdf')

            # Reading generated pdf document from soffice and adding it to our model field
            f = open(pdf_converted_loc, 'rb')
            myfile = DjangoFile(f)  # Converting to django's File model object
            # self.pdf_converted_file = myfile
            # self.pdf_converted_file.name = file_with_pdf_ext
            doc = Document.objects.get(slug=request.POST['file'])
            subscription_obj = get_current_subscription(self.request.user)
            try:
                pay_per_doc_sub = self.request.user.pay_per_download.all()
                pay_per_doc = pay_per_doc_sub.get(documents=doc, expire_on__gt=timezone.now())
                if pay_per_doc:
                    self.payperdoc = True
                    remaining_downloads = 1
            except:
                remaining_downloads = 0
                if subscription_obj:
                    expiry_date_subscription = subscription_obj.expire_on
                    plan = subscription_obj.plan
                    plan_days = plan.days
                    plan_download_limit = plan.download_limit
                    startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
                    download_count = Download.objects.filter(user=self.request.user, created_at__gte=startdate_subscription,
                                                             created_at__lte=expiry_date_subscription, ).count()
                    remaining_downloads = plan_download_limit - download_count

            if remaining_downloads > 0 or self.payperdoc:
                slug = request.POST['file']
                try:
                    document_obj = Document.objects.get(slug=slug)
                    if not document_obj in subscription_obj.documents.all() and not self.payperdoc:
                        subscription_obj.documents.add(document_obj)
                        Download.objects.create(user=request.user, document=document_obj)
                        Document.objects.filter(pk=document_obj.pk).update(total_downloads=F('total_downloads') + 1)
                except Exception as e:
                    print(e)

                try:
                    attachments = {}
                    pdf_doc_name = myfile.name.split('/')[-1]
                    attachments[pdf_doc_name] = file_to_be_send = ContentFile(myfile.file.read())

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
                    from django.core.mail import send_mail
                    message = ''
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [request.user.email],
                    html_message = htmly
                    mail = EmailMultiAlternatives(
                        subject='Confirmation For Your Document Download',
                        to=[request.user.email],
                        body=''
                    )
                    # mail = EmailMultiAlternatives(subject, message, from_email, to=recipient_list)
                    mail.attach_alternative(html_message, 'text/html')
                    mail.attach(filename="Document.pdf", content=file_to_be_send.read(), mimetype='application/text')
                    mail.send(True)
                    # mail.send(
                    #     request.user.email,  # List of email addresses also accepted
                    #     settings.DEFAULT_FROM_EMAIL,
                    #     subject='Your downloaded document from desklib.com',
                    #     # message=htmly,
                    #     html_message=htmly,
                    #     attachments=attachments,
                    #     priority='now'
                    # )
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
            if self.payperdoc:
                return redirect('/document/download/success?doc=%s&pay-per-download=True' % (slug))
            else:
                return redirect('/document/download/success?doc=%s' % (slug))
        else:
            return render(request, self.template_name, {
                'form': form,
            })


class DocumentPayment(LoginRequiredMixin, MetadataMixin, TemplateView):
    template_name = 'documents/doc-payment.html'
    title = 'Homework Help Payment | Online Homework Help - Desklib'



    def get(self, request, *args, **kwargs):
        context = super(DocumentPayment, self).get(request, *args, **kwargs)
        subscription_obj = get_current_subscription(self.request.user)
        try:
            pay_per_doc_sub = self.request.user.pay_per_download.all()
        except:
            pay_per_doc_sub = None
        try:
            doc = Document.objects.get(slug=self.request.GET.get('doc'))
        except:
            return render(request, 'desklib/error_404.html', status=404)
        pay_per_doc_obj = pay_per_doc_sub.filter(documents=doc, expire_on__gt=timezone.now())
        if subscription_obj:
            expiry_date_subscription = subscription_obj.expire_on
            plan = subscription_obj.plan
            plan_download_limit = plan.download_limit

            plan_days = plan.days
            startdate_subscription = expiry_date_subscription - timedelta(days=plan_days)
            download_count = Download.objects.filter(user=self.request.user, created_at__gte=startdate_subscription,
                                                     created_at__lte=expiry_date_subscription).count()
            remaining_downloads = plan_download_limit - download_count
            if remaining_downloads > 0:
                return redirect("%s?doc=%s" % (redirect('documents:download-info-view').url, doc.slug))
        elif pay_per_doc_obj:
            return redirect("%s?doc=%s" % (redirect('documents:download-info-view').url, doc.slug))
        return context

    def get_context_data(self, **kwargs):
        context = super(DocumentPayment, self).get_context_data(**kwargs)


        # reader = geoip2.database.Reader('desklib/GeoLite2-City_20200609/GeoLite2-City.mmdb')
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        if not ip == '127.0.0.1':
            try:
                response = GeoIP2().city(ip)
                country = response.get('country_code')
                timezone  = response.get('time_zone')
                context['location'] = country
            except:
                context['location'] = None

        context['plan_qs'] = Plan.objects.all()
        context['payperdoc'] = PayPerDocument.objects.all()
        context['doc'] = self.request.GET.get('doc')
        context['user'] = self.request.user
        context['form1'] = UploadForm
        context['form2'] = UploadFileForm

        context['tracking_id'] = key_generator()
        if settings.PAYPAL_TEST:
            receiver_email = "info-facilitator@a2zservices.net"
        else:
            receiver_email = "info@a2zservices.net"
        paypal_dict = {
            "business": receiver_email,
            "item_name": "desklib subscription",
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return": self.request.build_absolute_uri('../paypal/redirect/' + self.request.GET.get('doc')),
            "cancel_return": self.request.build_absolute_uri('../' + self.request.GET.get('doc')),

        }

        form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
        context['form'] = form
        return context


class PaypalDocumentRedirect(RedirectView):
    def get(self, request, *args, **kwargs):
        messages.success(request,
                         'Your payment is being processed. Please access your document once you recieve an email regarding your activation.')
        return redirect(self.request.build_absolute_uri('../../%s' % (kwargs.get('slug'))))


class DocumentDownloadView(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        # print(request.user)
        try:
            pay_per_doc_sub = self.request.user.pay_per_download.all()
        except:
            pass
        if request.user.subscriptions.all().exists() or pay_per_doc_sub:
            subscription_obj = get_current_subscription(self.request.user)
            try:
                doc = Document.objects.get(slug=request.GET.get('slug'))
            except:
                doc = Document.objects.get(slug=request.GET.get('doc'))
            pay_per_doc_obj = pay_per_doc_sub.filter(documents=doc, expire_on__gt=timezone.now())
            if subscription_obj or pay_per_doc_obj:
                # return redirect('documents:download-info-view', slug=request.GET.get('doc'))
                return redirect("%s?doc=%s" % (redirect('documents:download-info-view').url, doc.slug))
            else:
                return redirect('subscription')
        else:
            return redirect('subscription')


class DownloadSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/download_success.html'

    def get_context_data(self, **kwargs):
        context = super(DownloadSuccessView, self).get_context_data(**kwargs)
        if bool(self.request.GET.get('pay-per-download')):
            context['doc_slug'] = self.request.GET.get('doc')
        else:
            try:
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
                context['doc_slug'] = self.request.GET.get('doc')

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


class FilterSimlar():
    def fiterSimilar(self):
        return SearchQuerySet.raw_search(
            mlt_query={
                'query': {
                    'more_like_this': {
                        'like': [{
                            "_id": 1
                        }],
                        'minimum_should_match': '100%'
                    }
                }
            }

        )


@method_decorator(staff_member_required, name='dispatch')
class DocumentSearchDescription(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = 'admin/search_in_description.html'
    permission_required = 'documents.search_in_description'
    raise_exception = True
    form_class = DocumentSearchForm

    def post(self, request, *args, **kwargs):
        form = DocumentSearchForm(self.request.POST)
        sqs = SearchQuerySet().models(Document).filter(description=request.POST['search'])
        file = SearchQuerySet().models(Document).filter(file_name=request.POST['search'])
        result = sqs | file

        return TemplateResponse(request, "admin/search_in_description.html", context={'result':result, 'form': form})




class PaypalPaymentCheckView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))

        # if settings.DEBUG:
        url = settings.PAYPAL_TOKEN_API

        data = {
            "grant_type": "client_credentials"
        }
        headers = {
            'content-type': "application/x-www-form-urlencoded",
        }
        client = settings.PAYPAL_CLIENT
        secret = settings.PAYPAL_SECRET

        auth = (client, secret)

        auth_token = requests.request("POST", url, data=data, headers=headers, auth=auth)
        token = json.loads(auth_token.text).get('access_token')
        # else:
        #     f = open(settings.BASE_DIR + "/"+settings.AUTHTOKEN, "r")
        #     token = f.read()

        url = settings.PAYPAL_RISK_API + settings.PAYPAL_MERCHANT_ID + "/" + body.get('tracking_id')

        payload = json.dumps({
            "tracking_id": body.get('tracking_id'),
            "additional_data": [
                {
                    "key":"sender_first_name",
                    "value": request.user.first_name
                },
                {
                    "key":"sender_email",
                    "value": request.user.email
                },
                {
                    "key":"sender_phone",
                    "value": str(request.user.contact_no)
                },
                {
                    "key":"sender_country_code",
                    "value": str(request.user.country)
                },
                {
                    "key":"sender_create_date",
                    "value": str(datetime.now())
                },
            ],
        })
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'accept-language': "en_US",
            'authorization': "Bearer " + str(token)
        }

        risk_response = requests.request("PUT", url, data=payload, headers=headers)

        # print(auth_token.status_code)
        #
        # print(auth_token.text)

        payment_invoice = PaypalInvoice(user=request.user)
        payment_invoice.save()

        url = settings.PAYPAL_CHECKOUT_API

        plan_key = body.get('key')
        plan = Plan.objects.get(key=plan_key)
        amount = plan.price

        payload = json.dumps({
  "intent": "CAPTURE",
  "application_context":{
    "brand_name":"Desklib",
    # "locale":"en-US",
    "shipping_preference":"NO_SHIPPING",
    "user_action":"PAY_NOW",
    # "return_url":"http://ReturnURL",
    # "cancel_url":"http://CancelURL",
    "payment_method":{
        "payer_selected":"PAYPAL",
		 "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
    }
  },
  "payer":{
    "name":{
        "given_name": request.user.first_name,
        "surname": request.user.last_name
    },
    "email_address": request.user.email,
    # "phone": {
    #         "phone_number": {
    #             "national_number": request.user.contact_no.national_number
    #         }
    #     }
    },
  "purchase_units": [
    {
        "amount": {
              "currency_code": "USD",
              "value": amount,
              "breakdown": {
                "item_total": {
                  "currency_code": "USD",
                  "value": amount
                }
              }
            },
        "items": [
            {
              "name": plan.package_name,
              "quantity": "1",
              "category": "DIGITAL_GOODS",
              "unit_amount": {
                "currency_code": "USD",
                "value": amount
              }
            }],
        "soft_descriptor":"Desklib",
	    # "custom_id": tracking_id,	#// Pass any custom value of website if required
	    "invoice_id": payment_invoice.invoice_id #// Pass the unique order id of website
    }
  ]
})
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'accept-language': "en_US",
            'authorization': "Bearer "+str(token)
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return HttpResponse(response, content_type='application/json')


class PaypalPaymentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        # if settings.DEBUG:
        url = settings.PAYPAL_TOKEN_API

        data = {
            "grant_type": "client_credentials"
        }
        headers = {
            'content-type': "application/x-www-form-urlencoded",
        }
        client = settings.PAYPAL_CLIENT
        secret = settings.PAYPAL_SECRET

        auth = (client, secret)

        auth_token = requests.request("POST", url, data=data, headers=headers, auth=auth)
        token = json.loads(auth_token.text).get('access_token')
        # else:
        #     f = open(settings.BASE_DIR + "/"+settings.AUTHTOKEN, "r")
        #     token = f.read()

        body = json.loads(request.body.decode("utf-8"))

        url = settings.PAYPAL_CHECKOUT_API + "/" + body.get('orderid') + "/capture"

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+str(token),
            'PayPal-Client-Metadata-Id': body.get('tracking_id'),
            'PayPal-Request-id': key_generator()
        }

        response = requests.request("POST", url, headers=headers)

        # print(response.status_code)
        #
        # print(response.text)
        resp_json = json.loads(response.text)

        invoice_id = resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('invoice_id')
        payment = PaypalInvoice.objects.get(invoice_id=invoice_id)
        payment.buyer_email = resp_json.get('payer').get('email_address')
        payment.amount = resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get('value')
        payment.status = resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('status')
        payment.currency = resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get("currency_code")
        payment.transaction_id = resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('id')
        payment.save()

        # print(body)
        if settings.DEBUG:
            receiver_email = "ankushtambi-facilitator@gmail.com"
            # receiver_email = "info-facilitator@a2zservices.net"
            # action="https://www.sandbox.paypal.com/cgi-bin/webscr

            # homework help payment logic
        else:
            receiver_email = "payment@locusrags.com"
        if resp_json.get('status') == "COMPLETED":

            email = body.get('user')
            plan_key = body.get('key')
            try:
                doc_slug = body.get('doc')
                doc = Document.objects.get(slug=doc_slug)
            except:
                pass
            plan = Plan.objects.get(key=plan_key)
            plan_days = plan.days
            pay_date = datetime.strptime(resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('create_time'), '%Y-%m-%dT%H:%M:%SZ')
            payment_date = pytz.utc.localize(pay_date)
            expire_on = payment_date + timedelta(days=plan_days)
            user = UserAccount.objects.get(email=email)
            site_url = Site.objects.get_current().domain
            amount = int(float(resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get('value')))

            if amount==plan.price:
                if plan.is_pay_per_download:
                    contex = {'traction_id': resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('id'), 'currency': resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get("currency_code"),
                              'amount': resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get('value'), 'payment_date': str(payment_date.date()),
                              'expiry': str(expire_on),
                              'plan': plan.package_name, 'document_redirect': doc_slug, 'SITE_URL': site_url, }
                    # pay_doc = PayPerDocument.objects.filter(user=user, start_date=payment_date,documents=doc, expire_on=expire_on)
                    # if pay_doc :
                    #     pay_doc.documents.add(doc)
                    payperdoc = PayPerDocument.objects.create(user=user, plan=plan, expire_on=expire_on,
                                                              start_date=payment_date, is_current=True)
                    payperdoc.documents.add(doc)
                    messages.success(request, 'Congratulations! You have successfully unlocked this document.')
                else:
                    contex = {'traction_id': resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('id'), 'currency': resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get("currency_code"),
                              'amount': resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get('value'), 'payment_date': str(payment_date.date()),
                              'expiry': str(expire_on),
                              'plan': plan.package_name, 'SITE_URL': site_url, }
                    subscription = Subscription.objects.create(user=user, plan=plan, expire_on=expire_on,
                                                               author=user)

                    messages.success(request, 'Congratulations! You have successfully subscribed to ' + plan.package_name + '.')
                try:

                    htmly = render_to_string('desklib/mail-templates/payment_success_email_template.html',
                                             context=contex, request=None)
                    html_message = htmly
                    mail = EmailMultiAlternatives(
                        subject='Payment Success Confirmation From Desklib',
                        to=[user.email],
                        body=''
                    )
                    mail.attach_alternative(html_message, 'text/html')
                    mail.send(True)

                except Exception as e:
                    print("Payment Success Email Sending failed", e)
            else:
                try:
                    amount = body.get('purchase_units')[0].get("amount").get("value")
                    locus_email = "kushagra.goel@locusrags.com"
                    if not settings.DEBUG:
                        locus_email = "info@desklib.com"
                    if amount != plan.price:
                        amount_remaining = plan.price - body.get('purchase_units')[0].get("amount").get("value")
                        html_message = "Plan Name: "+ str(plan) + "<br>Payment done by user: "+ user.username + "<br>Amount Received: " + str(amount) + "<br>AmountPending: " + str(amount_remaining) + "<br>For Document: " + str(doc)
                        mail = EmailMultiAlternatives(
                            subject='Insufficient Amount received from Client',
                            # from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[locus_email],
                            body=''
                        )
                        mail.attach_alternative(html_message, 'text/html')
                        mail.send(True)
                    else:
                        pass
                except:
                    pass

            # messages.success(request, 'Congratulations! You have successfully unlocked this document.')
            # return redirect(reverse('documents:document-view', kwargs={'slug': doc.slug}))
            return JsonResponse('Payment completed', safe=False)
        else:
            return
