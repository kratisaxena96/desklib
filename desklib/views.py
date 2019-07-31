from django.views.generic.base import TemplateView

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.conf import settings
import logging
from django.views.generic.edit import FormView
from haystack.generic_views import SearchView
from django_json_ld import settings as setting
from documents.models import Document
from.forms import HomeSearchForm
logger = logging.getLogger(__name__)

class HomePageView(MetadataMixin,JsonLdContextMixin,SearchView):
    form_class = HomeSearchForm
    title = 'Library at your desk | desklib.com'
    description = 'Desklib is your home for best study resources and educational documents. We have a large collection of homework answers, assignment solutions, reports and presentations. Our automated tools help you improve your writing skills and grammar.'
    keywords = ['Study resources','study material','homework solution', 'study tools', 'educational documents']
    twitter_title = 'All study resources you will need to secure best grades.'

    template_name = "desklib/home.html"
    # template_name = "desklib/coming_soon.html"

    structured_data = {
        "@type": "Organization",
        "name": "DeskLib",
        "description": _("All study resources you will need to secure best grade."),
        "url": "https://desklib.com/",
        "logo": "https://www.desklib.com/assets/img/desklib_logo.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.youtube.com/desklib",
            "https://www.pinterest.com/desklib/",
            "https://www.instagram.com/desklib/",
            "https://plus.google.com/+desklib",
            "https://en.wikipedia.org/wiki/desklib",
            "https://github.com/desklib"
        ]
    }

    def get_structured_data(self):
        sd = super(HomePageView, self).get_structured_data()
        return sd

    def get_context_data(self, **kwargs):
        context = super(JsonLdContextMixin, self).get_context_data(**kwargs)
        context[self.context_meta_name] = self.get_meta(context=context)
        context[setting.CONTEXT_ATTRIBUTE] = self.get_structured_data()
        top_results = list(Document.objects.all().order_by('views')[:5])
        # cover_image = top_results.pages.first().image_file.name
        context['top_results'] = top_results
        # context['cover_image'] = cover_image
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return context


class AboutPageView(MetadataMixin,JsonLdContextMixin,TemplateView):
    title = 'About | desklib.com'
    description = 'DeskLib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades.'

    template_name = "desklib/about.html"

    structured_data = {
        "@type": "Organization",
        "name": "DeskLib",
        "description": _("DeskLib is a single stop solution for all your academic needs. We provide millions of study documents which can be used for by students to obtain better grades."),
        "url": "https://desklib.com/",
        "logo": "https://www.desklib.com/assets/img/desklib_logo.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.youtube.com/desklib",
            "https://www.pinterest.com/desklib/",
            "https://www.instagram.com/desklib/",
            "https://plus.google.com/+desklib",
            "https://en.wikipedia.org/wiki/desklib",
            "https://github.com/desklib"
        ]
    }

    def get_structured_data(self):
        sd = super(AboutPageView, self).get_structured_data()
        return sd


class PricingPageView(MetadataMixin,JsonLdContextMixin,TemplateView):
    title = 'Pricing | desklib.com'
    description = 'DeskLib provides a subscription based access to its resources at affordable price.'
    template_name = "desklib/pricing.html"

    structured_data = {
        "@type": "Organization",
        "name": "DeskLib",
        "description": _(
            'DeskLib provides a subscription based access to its resources at affordable price.'),
        "url": "https://desklib.com/",
        "logo": "https://www.desklib.com/assets/img/desklib_logo.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.youtube.com/desklib",
            "https://www.pinterest.com/desklib/",
            "https://www.instagram.com/desklib/",
            "https://plus.google.com/+desklib",
            "https://en.wikipedia.org/wiki/desklib",
            "https://github.com/desklib"
        ]
    }

    def get_structured_data(self):
        sd = super(PricingPageView, self).get_structured_data()
        return sd


class ContactPageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Contact | desklib.com'
    description = '24X7 online support for our customers. Reach our customer support and get your queries answered instantly.'

    template_name = "desklib/contact.html"

    structured_data = {
        "@type": "Organization",
        "name": "DeskLib",
        "description": _(
            '24X7 online support for our customers. Reach our customer support and get your queries answered instantly.'),
        "url": "https://desklib.com/",
        "logo": "https://www.desklib.com/assets/img/desklib_logo.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.youtube.com/desklib",
            "https://www.pinterest.com/desklib/",
            "https://www.instagram.com/desklib/",
            "https://plus.google.com/+desklib",
            "https://en.wikipedia.org/wiki/desklib",
            "https://github.com/desklib"
        ]
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

