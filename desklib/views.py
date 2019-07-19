from django.views.generic.base import TemplateView

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class HomePageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Home page'
    description = 'This is an awesome page hey'
    keywords = ['Our','best','homepage']
    twitter_title = 'Hello Twitter'

    template_name = "desklib/home.html"
    # template_name = "desklib/coming_soon.html"

    structured_data = {
        "@type": "Organization",
        "name": "The Company home",
        "description": _("A great company."),
    }

    def get_structured_data(self):
        sd = super(HomePageView, self).get_structured_data()
        return sd


class AboutPageView(MetadataMixin,JsonLdContextMixin,TemplateView):
    title = 'About page'
    description = 'This is an About page'

    template_name = "desklib/about.html"

    structured_data = {
        "@type": "Organization",
        "name": "The Company home",
        "description": _("ABOUT company."),
    }

    def get_structured_data(self):
        sd = super(AboutPageView, self).get_structured_data()
        return sd


class PricingPageView(MetadataMixin,JsonLdContextMixin,TemplateView):
    title = 'Pricing page'
    description = 'This is a Pricing page'

    template_name = "desklib/pricing.html"

    structured_data = {
        "@type": "Organization",
        "name": "The Company home",
        "description": _("Pricing company."),
    }

    def get_structured_data(self):
        sd = super(PricingPageView, self).get_structured_data()
        return sd


class ContactPageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Contact page'
    description = 'This is a contact page'

    template_name = "desklib/contact.html"

    structured_data = {
        "@type": "Organization",
        "name": "The Company home",
        "description": _("A Contact company."),
    }

    def get_structured_data(self):
        sd = super(ContactPageView, self).get_structured_data()
        return sd


class TestPageView(TemplateView):
    template_name = "desklib/test.html"


def handler404(request, *args, **kwargs):
    if settings.DEBUG:
        return render(request,'desklib/error_404.html', status=404)
    else:
        return render(request, 'desklib/error_404.html', status=404)


def handler500(request, *args, **kwargs):
    if settings.DEBUG:
        return render(request,'desklib/error_500.html', status=500)
    else:
        return render(request, 'desklib/error_500.html', status=500)