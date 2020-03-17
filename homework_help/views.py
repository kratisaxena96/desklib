from django.contrib.auth.mixins import LoginRequiredMixin
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from haystack.generic_views import SearchView
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView, DetailView
from homework_help.models import Order, Comment, Question
from homework_help.forms import CommentForm, QuestionForm

# Create your views here.


class OrderDetailView(LoginRequiredMixin, FormView):
    model = Order
    template_name = 'homework_help/order_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order = Order.objects.get(order_id=self.kwargs['order_id'])
        context['order'] = order
        return context


class AskQuestionView(FormView):
    template_name = 'homework_help/ask_question.html'
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        context = super(AskQuestionView, self).get_context_data(**kwargs)
        # order = Order.objects.get(order_id=self.kwargs['order_id'])
        # context['order'] = order
        return context


class QuestionDetailView(LoginRequiredMixin, TemplateView):
    model = Question
    template_name = "homework_help/question_detail.html"
    # template_name = "desklib/coming_soon.html"
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
        context['object'] = question
        # context[self.context_meta_name] = self.get_meta(context=context)
        return context


class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = "homework_help/order_create.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):

        context = super(OrderCreateView, self).get_context_data(**kwargs)
        question = self.request.GET.get('question')
        question_object = Question.objects.get(slug=question)

        if settings.PAYPAL_TEST:
            receiver_email = "info-facilitator@a2zservices.net"
        else:
            receiver_email = "info@a2zservices.net"
        paypal_dict = {
            "business": receiver_email,
            "item_name": "desklib subscription",
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return": self.request.build_absolute_uri('../paypal/redirect/'+self.request.GET.get('question')),
            "cancel_return": self.request.build_absolute_uri('../'+self.request.GET.get('question')),

        }

        form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
        context['form'] = form

        context['question'] = question_object
        return context

