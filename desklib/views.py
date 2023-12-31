import logging
import Adyen
from django.views.generic.base import TemplateView
from haystack.query import SearchQuerySet
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from haystack.generic_views import SearchView
from django_json_ld import settings as setting

from desklib.mixins import CheckSubscriptionMixin
from documents.models import Document
from .forms import HomeSearchForm
from subscription.models import Plan
from django.utils import timezone
from homework_help.forms import QuestionForm, QuestionHomeForm

from subscription.utils import get_current_subscription
import pytz

logger = logging.getLogger(__name__)


class ComingSoonPageView(MetadataMixin, JsonLdContextMixin, TemplateView):
    form_class = HomeSearchForm
    title = 'Best study and educational resources | desklib.com'
    description = 'Desklib is your home for best study resources and educational documents. We have a large collection of homework answers, assignment solutions, reports, sample resume and presentations. Our study tools help you improve your writing skills and grammar.'
    keywords = ['study resources', 'study material', 'homework solution', 'study tools', 'online tutoring',
                'educational documents', 'sample resume']
    twitter_title = 'All study resources you will need to secure best grades in your assignments'
    og_title = 'All study resources you will need to secure best grades in your assignments'
    gplus_title = 'All study resources you will need to secure best grades in your assignments'

    template_name = "desklib/coming_soon.html"

    structured_data = {
        "@type": "Organization",
        "name": "Desklib",
        "description": _("All study resources you will need to secure best grade."),
        "url": "https://desklib.com/",
        "logo": "https://desklib.com/assets/img/desklib_logo.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_structured_data(self):
        sd = super(ComingSoonPageView, self).get_structured_data()
        return sd

class AdmissionsView(MetadataMixin, JsonLdContextMixin, TemplateView):
    title = 'Admission page | desklib.com'
    # title = 'About us | about desklib online learning library | online solutions '
    # description = 'Desklib is a single stop solution for all your academic needs. We provide millions of study documents including assignment solutions which can help students achieve better grades.'
    description = 'We as the best choice among students of Aus, UK, USA, and leading towards the globe to become the best online learning library and homework help Service provider Company in the World. Consult our highly-qualified and experienced writers to attain academic excellence.'
    keywords = ['assignment help', 'online learning library', 'homework help websites', 'online dissertation help',
                'online thesis writing services', 'college assignment help online', 'college homework help']
    template_name = "desklib/admissions.html"

    structured_data = {
        "@type": "Organization",
        "name": "Desklib",
        "description": _(
            "Desklib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades."),
        "url": "https://desklib.com/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }


class HomePageView(MetadataMixin, JsonLdContextMixin, SearchView):
    form_class = HomeSearchForm
    form_class2 = QuestionHomeForm
    title = 'Desklib | Online Homework Help | Homework Solutions'
    # description = 'Desklib is your home for best study resources and educational documents. We have a large collection of homework answers, assignment solutions, reports, sample resume and presentations. Our study tools help you improve your writing skills and grammar.'
    description = 'Get affordable homework solutions or online homework help from our library. Avail math, science, english and all subjects college homework help at affordable prices.'
    keywords = ['homework solutions', 'online homework help', 'College Homework Help', 'Homework Helper']
    twitter_title = 'Desklib | Online Homework Help | Homework Solutions'
    og_title = 'Desklib | Online Homework Help | Homework Solutions'

    template_name = "desklib/v2/home.html"

    structured_data = {
        "@type": "Organization",
        "name": "Desklib | Online Homework Help | Homework Solutions",
        "description": _("Get homework solutions by desklib online homework help library. Avail math, science, english and all subjects college homework help at affordable prices."),
        "url": "https://desklib.com/",
        "logo": "https://desklib.com/assets/img/desklib_logo.png",
        # "potentialAction": {
        #     "@type": "SearchAction",
        #     "target": "https://desklib.com/study/search/?q={search_term}",
        #     "query-input": "required name=search_term"
        # },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_structured_data(self):
        sd = super(HomePageView, self).get_structured_data()
        return sd

    def get_context_data(self, **kwargs):
        context = super(JsonLdContextMixin, self).get_context_data(**kwargs)
        context[self.context_meta_name] = self.get_meta(context=context)
        context[setting.CONTEXT_ATTRIBUTE] = self.get_structured_data()
        top_results = SearchQuerySet().order_by('-views')[:6]
        # cover_image = top_results.pages.first().image_file.name
        # top_results = Document.objects.all().order_by('-views')[:6]
        context['top_results'] = top_results
        # context['cover_image'] = cover_image
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if 'form2' not in context:
            context['form2'] = QuestionHomeForm
        return context



class AboutPageView(MetadataMixin, JsonLdContextMixin, TemplateView):
    title = 'About us | about desklib online learning library | online solutions '
    # description = 'Desklib is a single stop solution for all your academic needs. We provide millions of study documents including assignment solutions which can help students achieve better grades.'
    description = 'We as the best choice among students of Aus, UK, USA, and leading towards the globe to become the best online learning library and homework help Service provider Company in the World. Consult our highly-qualified and experienced writers to attain academic excellence.'
    keywords= ['assignment help', 'online learning library', 'homework help websites', 'online dissertation help', 'online thesis writing services', 'college assignment help online', 'college homework help']
    template_name = "desklib/v2/about.html"

    structured_data = {
        "@type": "Organization",
        "name": "Desklib",
        "description": _(
            "Desklib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades."),
        "url": "https://desklib.com/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_structured_data(self):
        sd = super(AboutPageView, self).get_structured_data()
        return sd


class PricingPageView(MetadataMixin, JsonLdContextMixin, TemplateView):
    title = 'Pricing | desklib.com'
    description = 'Desklib provides a subscription based access to its resources at affordable price.'
    template_name = "desklib/pricing.html"

    structured_data = {
        "@type": "Organization",
        "name": "Desklib",
        "description": _(
            'Desklib provides a subscription based access to its resources at affordable price.'),
        "url": "https://desklib.com/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_structured_data(self):
        sd = super(PricingPageView, self).get_structured_data()
        return sd


class ContactPageView(MetadataMixin, JsonLdContextMixin, TemplateView):
    title = 'Contact | desklib.com'
    # description = '24X7 online support for our customers. Reach our customer support and get your queries answered instantly.'
    description = 'If any of you need online assignment help,homework help or dissertation help services,you can contact us through email or via phone.'
    keywords = [ 'homework help', 'online assignment help', 'dissertation help', 'thesis writing help online', 'dissertation writing service uk', 'college assignment help', 'online homework help']
    template_name = "desklib/v2/contact.html"

    structured_data = {
        "@type": "Organization",
        "name": "Desklib",
        "description": _(
            '24X7 online support for our customers. Reach our customer support and get your queries answered instantly.'),
        "url": "https://desklib.com/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_structured_data(self):
        sd = super(ContactPageView, self).get_structured_data()
        return sd


class TestPageView(TemplateView):
    template_name = "desklib/test.html"


def handler404(request, *args, **kwargs):
    if settings.DEBUG:
        return render(request, 'desklib/error_404.html', status=404)
    else:
        return render(request, 'desklib/error_404.html', status=404)


def handler500(request, *args, **kwargs):
    if settings.DEBUG:
        return render(request, 'desklib/error_500.html', status=500)
    else:
        return render(request, 'desklib/error_500.html', status=500)


class PaypalPaymentView(TemplateView):
    template_name = "desklib/payment.html"

    def get_context_data(self, **kwargs):
        context = super(PaypalPaymentView, self).get_context_data(**kwargs)
        if settings.PAYPAL_TEST:
            receiver_email = "info-facilitator@a2zservices.net"
            # action="https://www.sandbox.paypal.com/cgi-bin/webscr"
        else:
            receiver_email = "info@a2zservices.net"

        paypal_dict = {
            "cmd": "_xclick-subscriptions",
            "a3": "9.99",  # monthly price
            "p3": 1,  # duration of each unit (depends on unit)
            "t3": "M",  # duration unit ("M for Month")
            "src": "1",  # make payments recur
            "sra": "1",  # reattempt payment on payment error
            "no_note": "1",  # remove extra notes (optional)
            "business": receiver_email,
            "amount": "10.00",
            "item_name": "name of the item",
            "invoice": "wko7u-",
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return": self.request.build_absolute_uri(reverse('about')),
            "cancel_return": self.request.build_absolute_uri(reverse('contact')),
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }

        form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
        context = {"form": form}
        return context


class SubscriptionView(MetadataMixin, JsonLdContextMixin, TemplateView):
    template_name = 'desklib/subscription.html'
    title = 'Get subscription | homework help | online learning library'
    description = 'Get a subscription of Desklib online learning library for homework help, assignment help, case study and dissertation help by filling up your requirements and secure better grades.'
    keywords = ['online learning library', 'homework help', 'dissertation writing help', 'assignment help', 'case study help ']

    def get_context_data(self, **kwargs):
        context = super(SubscriptionView, self).get_context_data(**kwargs)
        context['plan_qs'] = Plan.objects.filter(is_pay_per_download=False)
        return context


class PayNowView(LoginRequiredMixin, CheckSubscriptionMixin, TemplateView):
    template_name = 'desklib/paynow.html'

    def get_context_data(self, **kwargs):
        context = super(PayNowView, self).get_context_data(**kwargs)
        plan_key = kwargs.get('key')
        plan = Plan.objects.get(key=plan_key)
        context['plan'] = plan

        if settings.PAYPAL_TEST:
            receiver_email = "info-facilitator@a2zservices.net"
            # action="https://www.sandbox.paypal.com/cgi-bin/webscr"
        else:
            receiver_email = "info@a2zservices.net"
        now = timezone.now()

        if not self.request.user.subscriptions.all().filter(expire_on__gt=now):
            paypal_dict = {
                "business": receiver_email,
                "amount": plan.price,
                "item_name": "desklib subscription",
                # "invoice": "unique-invoice-id",
                "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
                "return": self.request.build_absolute_uri(reverse('payment_success')),
                "cancel_return": self.request.build_absolute_uri(reverse('payment_cancelled')),
                "custom": self.request.user.username + "_" + plan_key,
            # Custom command to correlate to some function later (optional)
            }

            form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
            context['form'] = form
        return context


class TermsOfUseView(MetadataMixin, TemplateView):
    title = 'Terms of use | desklib.com'
    description = 'Desklib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades.'
    template_name = "desklib/termsofuse.html"


class PrivacyPolicyView(MetadataMixin, TemplateView):
    title = 'Privacy Policy | desklib.com'
    description = 'Desklib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades.'
    template_name = "desklib/privacypolicy.html"


class CopyrightPolicyView(MetadataMixin, TemplateView):
    title = 'Copyright Policy | desklib.com'
    description = 'Desklib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades.'
    template_name = "desklib/copyrightpolicy.html"


class AcademicIntegrityView(MetadataMixin, TemplateView):
    title = 'Academic Integrity | desklib.com'
    description = 'Desklib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades.'
    template_name = "desklib/academicintegrity.html"


class HonorCodeView(MetadataMixin, TemplateView):
    title = 'Honor Code | desklib.com'
    description = 'Desklib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades.'
    template_name = "desklib/honorcode.html"


class PaymentCancelledView(LoginRequiredMixin,MetadataMixin, TemplateView):
    title = 'Payment Cancel | desklib.com'
    template_name = 'desklib/payment_cancelled.html'


class PaymentSuccessView(LoginRequiredMixin,MetadataMixin,TemplateView):
    title = 'Payment Success | desklib.com'
    template_name = 'desklib/payment_success.html'


class AlreadySubscribedView(LoginRequiredMixin,MetadataMixin, TemplateView):
    title = 'Already Subscribed | desklib.com'
    template_name = 'desklib/already_subscribed.html'


class Error404View(TemplateView):
    template_name = "desklib/error_404.html"


class Error500View(TemplateView):
    template_name = "desklib/error_500.html"


# class PaymentAdyenView(AdyenRedirectView):
#     # template_name = "desklib/test-pages/adyen-payment.html"
#     # model = MyModel
#
#     def get_form_kwargs(self):
#         order = self.get_object()
#         params = self.get_signed_order_params(order)
#
#         kwargs = super(PaymentAdyenView, self).get_form_kwargs()
#         kwargs.update({'initial': params})
#         return kwargs
#
#     def get_next_url(self):  # This is to populate the resURL
#         order = self.get_object()
#         return reverse('my_project:confirmation', kwargs={'pk': order.id})

