from django.views.generic.base import TemplateView

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _



class HomePageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Home page'
    description = 'This is an awesome page hey'
    keywords = ['Our','best','homepage']
    twitter_title = 'Hello Twitter'

    template_name = "desklib/home.html"

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

    template_name = "desklib/home.html"

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


class StudyPageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Study page'
    description = 'This is a Study page'

    template_name = "desklib/study.html"

    structured_data = {
        "@type": "Organization",
        "name": "The Company home",
        "description": _("A Contact company."),
    }

    def get_structured_data(self):
        sd = super(StudyPageView, self).get_structured_data()
        return sd

class WritingPageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Writing page'
    description = 'This is a Writing page'

    template_name = "desklib/writing.html"

    structured_data = {
        "@type": "Organization",
        "name": "This is writing Company home",
        "description": _("A writing company."),
    }

    def get_structured_data(self):
        sd = super(WritingPageView, self).get_structured_data()
        return sd
