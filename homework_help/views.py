import requests

from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils import timezone
from email.header import Header
from email.mime.image import MIMEImage

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from haystack.query import SearchQuerySet
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from haystack.generic_views import SearchView
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView, DetailView

from documents.utils import key_generator
from homework_help.models import Order, Comment, Question, Answers
from homework_help.forms import CommentForm, QuestionForm, QuestionHomeForm
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.generic_views import SearchView
import simplejson as json
from haystack.generic_views import SearchView, FacetedSearchView

from django_json_ld import settings as setting
from django.utils.translation import gettext as _

# Create your views here.
from subjects.models import Subject, SubjectQuestionContent
from django.shortcuts import redirect, render
from desklib.utils import get_timezone
from documents.models import Document
from django.views import View
from datetime import datetime

from subscription.models import PaypalInvoice


def autocomplete(request):
    sqs = SearchQuerySet().models(Question).filter(content_auto=request.GET.get('q', ''))[:5]
    data = {}
    item = {}
    i = 0
    for result in sqs:
        item["question"] = result.text
        item["slug"] = result.slug
        data[i] = item
        item = {}
        i += 1
    the_data = json.dumps(data)
    return HttpResponse(the_data, content_type='application/json')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    template_name = 'homework_help/order_detail.html'
    form_class = CommentForm
    title = 'Desklib | homework help | online learning library | assignment solutions '
    description = 'Desklib online learning library provides you 24/7 Homework Help, Q&A help, and solutions to assignments, essays, dissertations, case studies and Best free writing tools for everyone to improve their writing skills.'
    keywords = [ 'assignment writing help', 'online learning library', 'uk assignment help', 'Q&A help', 'homework help', 'dissertation writing help', 'assignment help online', 'Case Study Help']
    # twitter_title = 'All study resources you will need to secure best grades in your assignments'
    # og_title = 'All study resources you will need to secure best grades in your assignments'
    # gplus_title = 'All study resources you will need to secure best grades in your assignments'

    def get(self, request, *args, **kwargs):

        order = Order.objects.get(uuid=self.kwargs['uuid'])
        if self.request.user == order.author:
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'desklib/error_404.html', status=404)

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order = Order.objects.get(uuid=self.kwargs['uuid'])


        if settings.PAYPAL_TEST:
            receiver_email = "info-facilitator@a2zservices.net"
        else:
            receiver_email = "info@a2zservices.net"
        paypal_dict = {
            "business": receiver_email,
            "item_name": "Order- " + order.order_id,
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return": self.request.build_absolute_uri(reverse('homework_help:order-detail-view', kwargs={'uuid': self.kwargs.get('uuid')})),
            "cancel_return": self.request.build_absolute_uri(reverse('homework_help:order-detail-view', kwargs={'uuid': self.kwargs.get('uuid')})),
            "custom": "homework-help_" + self.kwargs.get('uuid'),
            # "amount": order.budget,
        }

        paypalform = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
        context['paypalform'] = paypalform
        context['meta'] = self.get_object().as_meta(self.request)
        context['order'] = order
        context['tracking_id'] = key_generator()
        return context


class OrderListView(LoginRequiredMixin, MetadataMixin, ListView):
    model = Order
    template_name = 'homework_help/order_list.html'
    paginate_by = 6
    title = 'Orders'
    description = 'Desklib online learning library provides you 24/7 Homework Help, Q&A help, and solutions to assignments, essays, dissertations, case studies and Best free writing tools for everyone to improve their writing skills.'
    keywords = [ 'assignment writing help', 'online learning library', 'uk assignment help', 'Q&A help', 'homework help', 'dissertation writing help', 'assignment help online', 'Case Study Help']
    # twitter_title = 'All study resources you will need to secure best grades in your assignments'
    # og_title = 'All study resources you will need to secure best grades in your assignments'
    # gplus_title = 'All study resources you will need to secure best grades in your assignments'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        queryset = queryset.filter(author=self.request.user).order_by('created')
        return queryset


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        order_list = Order.objects.filter(author=self.request.user).order_by('created')
        paginator = Paginator(order_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            blog_page = paginator.page(page)
        except PageNotAnInteger:
            blog_page = paginator.page(1)
        except EmptyPage:
            blog_page = paginator.page(paginator.num_pages)

        context['object'] = blog_page
        return context


class AskQuestionView(JsonLdContextMixin, MetadataMixin, FormView):
    template_name = 'homework_help/ask_question.html'
    form_class = QuestionForm
    title = 'Desklib | Homework Help | Ask Q&A from online experts'
    description = 'Access quality study resources and get homework help and solutions to your assignments. Click here to ask question from our experts.'
    keywords = ['help with homework ', 'Online Homework Help', 'Homework Help', 'College Homework Help', 'homework online']
    twitter_title = 'Homework Help - Ask Q&A from Online experts - Desklib'
    og_title = 'Homework Help - Ask Q&A from Online experts - Desklib'
    gplus_title = 'Homework Help - Ask Q&A from Online experts - Desklib'

    structured_data = {
        "@type": "Organization",
        "name": "Desklib | Homework Help | Ask Q&A from online experts",
        "description": _(
            'Access quality study resources and get homework help and solutions to your assignments. Click here to ask question from our experts.'),
        "url": "https://desklib.com/homework-help/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_structured_data(self):
        sd = super(AskQuestionView, self).get_structured_data()
        return sd


    def get_context_data(self, **kwargs):
        # context = super(AskQuestionView, self).get_context_data(**kwargs)
        context = super(JsonLdContextMixin, self).get_context_data(**kwargs)
        context[setting.CONTEXT_ATTRIBUTE] = self.get_structured_data()
        queryset = Question.objects.filter(is_published=True, is_visible=True, published_date__lte=timezone.now()).order_by('-published_date')[:6]
        subject = Subject.objects.all()[:12]
        # order = Order.objects.get(order_id=self.kwargs['order_id'])
        context['question'] = queryset
        context['subject'] = subject
        context[self.context_meta_name] = self.get_meta(context=context)
        return context



class CustomSearchQuestionView(JsonLdContextMixin, MetadataMixin, FacetedSearchView):
    model = Question
    queryset = SearchQuerySet().models(Question)
    extra_context = {"questionsearch":"True"}
    facet_fields = ['subjects']
    paginate_by = 4
    selected_facets = ['subjects', 'p_subject']
    suggestions = {}

    def get_queryset(self):
        queryset = super(CustomSearchQuestionView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        sqs = SearchQuerySet().facet('subjects')
        sqs_count = sqs.facet_counts()
        context = super(CustomSearchQuestionView, self).get_context_data(**kwargs)
        # context[settings.CONTEXT_ATTRIBUTE] = self.get_structured_data()
        # context['sqs'] = sqs_count
        slug_list = []
        for sub_filter in sqs_count.get('fields').get('subjects'):
            slug_list.append(sub_filter[0])
        context['slug_faceit'] = Subject.objects.filter(slug__in=slug_list)
        context['parent'] = Subject.objects.filter(parent_subject__isnull=True).prefetch_related('subject_set')
        context['subject_facet'] = Subject.objects.all()
        suggest_string = SearchQuerySet().spelling_suggestion(self.request.GET.get('q', ''))
        if self.request.GET.get('q', '') != suggest_string:
            context['suggestion'] = suggest_string
        context['selected'] = self.request.GET.get('selected_facets')
        if not self.request.GET.get('q') and not self.request.GET.get('selected_facets'):
            context['is_empty'] = True
        # context.update({'object_list': SearchQuerySet().filter(no_of_pages__range=[1, 5])})
        # self.searchqueryset = SearchQuerySet().order_by('-pub_date')[:5]

        # if self.suggestions:
        #     context['suggestion'] = self.suggestions
        # """Insert the form into the context dict."""
        # if 'form' not in kwargs:
        #     kwargs['form'] = self.get_form()
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = "homework_help/question_detail.html"
    # form_class = HomeSearchForm
    # title = 'Desklib | homework help | online learning library | assignment solutions '
    # # description = 'Desklib is your home for best study resources and educational documents. We have a large collection of homework answers, assignment solutions, reports, sample resume and presentations. Our study tools help you improve your writing skills and grammar.'
    # description = 'Desklib online learning library provides you 24/7 Homework Help, Q&A help, and solutions to assignments, essays, dissertations, case studies and Best free writing tools for everyone to improve their writing skills.'
    # keywords = [ 'assignment writing help', 'online learning library', 'uk assignment help', 'Q&A help', 'homework help', 'dissertation writing help', 'assignment help online', 'Case Study Help']
    # twitter_title = 'All study resources you will need to secure best grades in your assignments'
    # og_title = 'All study resources you will need to secure best grades in your assignments'
    # gplus_title = 'All study resources you will need to secure best grades in your assignments'
    #
    #
    # structured_data = {
    #     "@type": "Organization",
    #     "name": "Desklib | homework help | online learning library | assignment solutions",
    #     "description": _("Desklib online learning library provides you 24/7 Homework Help, Q&A help, and solutions to assignments, essays, dissertations, case studies and Best free writing tools for everyone to improve their writing skills."),
    #     "url": "https://desklib.com/",
    #     "logo": "https://desklib.com/assets/img/desklib_logo.png",
    #     "potentialAction": {
    #         "@type": "SearchAction",
    #         "target": "https://desklib.com/study/search/?q={search_term}",
    #         "query-input": "required name=search_term"
    #     },
    #     "sameAs": [
    #         "https://www.facebook.com/desklib",
    #         "https://twitter.com/desklib",
    #         "https://www.linkedin.com/company/desklib",
    #         "https://www.instagram.com/desklib/"
    #     ]
    # }
    #
    # def get_structured_data(self):
    #     sd = super(QuestionDetailView, self).get_structured_data()
    #     return sd

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)

        question = Question.objects.get(slug=self.kwargs['slug'])
        answer = Answers.objects.filter(question=question)
        similar_questions = Question.objects.filter(subjects=question.subjects, is_published=True, is_visible=True, published_date__lte=timezone.now())[:6]
        context['meta'] = self.get_object().as_meta(self.request)
        context['object'] = question
        context['answer'] = answer.count()
        context['similar_questions'] = similar_questions
        # context[self.context_meta_name] = self.get_meta(context=context)
        return context


class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = "homework_help/order_create.html"
    form_class = CommentForm

    def get(self, request, *args, **kwargs):

        question = Question.objects.get(uid= self.kwargs.get('uid'))
        order = Order(question=question, author=request.user)
        # order.client_timezone = get_timezone(self.request)
        order.save()

        ip = "https://"+ Site.objects.get_current().domain


        locus_email = "kushagra.goel@locusrags.com"
        if not settings.DEBUG:
            locus_email = "info@desklib.com"

        subject = order.order_id + ' added'
        message = question.question + ' added!'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = locus_email,
        html_message = order.order_id +' is added by '+ order.author.email +'.<br>Question is '+ question.question + '<br>Link for the admin is: ' + ip + reverse('admin:homework_help_order_change', args=(order.id,))
        mail = EmailMultiAlternatives(subject, message, from_email, to)

        # if question.user_questionfiles:
        for i in question.user_questionfiles.all():

            mime_image = MIMEImage(i.file.read())
            mime_image.add_header('Content-ID', '<image>', filename=i.title)
            mail.attach(mime_image)


            # mail.attach_file(.path)
        mail.attach_alternative(html_message, 'text/html')
        mail.send(True)



        subject = order.order_id + ' added'
        message = question.question + ' added!'
        from_email = settings.DEFAULT_FROM_EMAIL
        to = order.author.email,
        contex = {'first_name': order.author.first_name, 'order_id': order.order_id,
                  'question': question.question, 'SITE_URL': ip,  'uuid': order.uuid }
        htmly = render_to_string('homework_help/mail-templates/order_added.html',
                                 context=contex, request=None)
        html_message = htmly
        # html_message = "Hello " + order.author.first_name + ",<br>Your order " + order.order_id + " is added.<br>Question is " + question.question + "<br>"
        mail = EmailMultiAlternatives(subject, message, from_email, to)

        # if question.user_questionfiles:


            # mail.attach_file(.path)
        mail.attach_alternative(html_message, 'text/html')
        mail.send(True)

        return HttpResponseRedirect(redirect_to=reverse('homework_help:order-detail-view', kwargs={'uuid': order.uuid}))


class ParentSubjectQuestionView(MetadataMixin, JsonLdContextMixin, DetailView):
    template_name = "homework_help/parent_subject_question.html"
    model = Subject
    form_class = QuestionHomeForm

    def get_context_data(self, **kwargs):
        context = super(ParentSubjectQuestionView, self).get_context_data(**kwargs)
        parent_subject = Subject.objects.get(slug=self.kwargs['slug'])
        child_subject = Subject.objects.filter(parent_subject=parent_subject)
        subject = SubjectQuestionContent.objects.filter(subject=parent_subject.id)

        all = SearchQuerySet().filter(p_subject=parent_subject)[:20]
        recent = SearchQuerySet().filter(p_subject=parent_subject).order_by('-pub_date')[:20]
        top_results = SearchQuerySet().filter(p_subject=parent_subject).order_by('-views')[:20]

        question = Question.objects.filter(subjects=parent_subject.id, is_visible=True, is_published=True)

        for i in child_subject:
            ques = Question.objects.filter(subjects=i.id, is_visible=True, is_published=True)
            question = question | ques

        question = question.order_by('-published_date')

        context['meta'] = self.get_object().as_meta(self.request)
        context['recent'] = recent
        context['top_results'] = top_results
        context['question'] = question
        context['subject'] = subject
        context['parent_subject'] = parent_subject
        if 'form' not in context:
            context['form'] = QuestionHomeForm
        return context


class HomeworkHelpPaypalPaymentCheckView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))

        if settings.DEBUG:
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
        else:
            f = open(settings.BASE_DIR + "/authtoken.txt", "r")
            token = f.read()

        tracking_id = key_generator()
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
            'authorization': "Bearer " + token
        }

        risk_response = requests.request("PUT", url, data=payload, headers=headers)

        url = settings.PAYPAL_CHECKOUT_API

        payment_invoice = PaypalInvoice(user=request.user)
        payment_invoice.save()

        order_id = body.get('order')
        order = Order.objects.get(uuid=order_id)
        data = {}
        item = {}
        # item['amount'] = order.budget
        # data['purchase_units'] = item

        payload = json.dumps({
            "intent": "CAPTURE",
            "application_context": {
                "brand_name": "Desklib",
                # "locale": "en-US",
                "shipping_preference": "NO_SHIPPING",
                "user_action": "PAY_NOW",
                # "return_url": "http://ReturnURL",
                # "cancel_url": "http://CancelURL",
                "payment_method": {
                    "payer_selected": "PAYPAL",
                    "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                }
            },
            "payer": {
                "name": {
                    "given_name": request.user.first_name,
                    "surname": request.user.last_name
                },
                "email_address": request.user.email,
                # "phone": {
                #     "phone_number": {
                #         "national_number": request.user.contact_no.national_number
                #     }
                # }
            },
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": order.budget,
                        "breakdown": {
                            "item_total": {
                                "currency_code": "USD",
                                "value": order.budget
                            }
                        }
                    },
                    "items": [
                        {
                            "name": order.question.question[0:15:],
                            "quantity": "1",
                            "unit_amount": {
                                "currency_code": "USD",
                                "value": order.budget
                            }
                        }],
                    "soft_descriptor":"Desklib",
                    # "custom_id":"12345",	#// Pass any custom value of website if required
                    "invoice_id": payment_invoice.invoice_id	#// Pass the unique order id of website
                }
            ]
        })
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'accept-language': "en_US",
            'authorization': "Bearer "+ token
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return HttpResponse(response, content_type='application/json')


class HomeworkHelpPaypalPaymentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        if settings.DEBUG:
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
        else:
            f = open(settings.BASE_DIR + "/authtoken.txt", "r")
            token = f.read()
        body = json.loads(request.body.decode("utf-8"))
        url = settings.PAYPAL_CHECKOUT_API + "/" + body.get('orderid') + "/capture"

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+ token,
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

            order = body.get('order')
            o = Order.objects.get(uuid=order)
            o.amount_paid = o.amount_paid + int(float(resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get('value')))
            time_split = o.expected_hours
            p = time_split
            if p:
                if p > 24:
                    total_days = p // 24
                    total_hours = p % 24
                    o.deadline_datetime = datetime.strptime(body.get('create_time'), '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(days=total_days, hours=total_hours)
                else:
                    total_hours = p
                    o.deadline_datetime = datetime.strptime(body.get('create_time'), '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=total_hours)

            o.status = 3
            o.save()

            ip = "https://" + Site.objects.get_current().domain

            subject = 'payment for ' + o.order_id + ' completed'
            message = 'payment for ' + o.order_id + ' completed'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = o.author.email,
            contex = {'first_name': o.author.first_name, 'order_id': o.order_id, 'SITE_URL': ip, 'uuid': o.uuid,
                      'amount': int(float(resp_json.get('purchase_units')[0].get('payments').get('captures')[0].get('amount').get('value')))}
            htmly = render_to_string('homework_help/mail-templates/order_payment_completed.html',
                                     context=contex, request=None)
            html_message = htmly
            # html_message = "Hello " + o.author.first_name + ",<br>Your order " + o.order_id + " is added.<br>Question is <br>"
            mail = EmailMultiAlternatives(subject, message, from_email, to)

            # if question.user_questionfiles:

            # mail.attach_file(.path)
            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)

            locus_email = "kushagra.goel@locusrags.com"
            if not settings.DEBUG:
                locus_email = "info@desklib.com"

            subject = 'payment for ' + o.order_id + ' recieved'
            message = 'payment for ' + o.order_id + ' recieved'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = locus_email,
            html_message = 'Hello<br>Payment for ' + o.order_id + ' recieved' + '<br>Link for the admin is: ' + ip + reverse(
                'admin:homework_help_order_change', args=(o.id,))
            mail = EmailMultiAlternatives(subject, message, from_email, to)

            # if question.user_questionfiles:

            # mail.attach_file(.path)
            mail.attach_alternative(html_message, 'text/html')
            mail.send(True)
            return JsonResponse('Payment completed', safe=False)

