from django.shortcuts import render

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _

from django.views.generic.edit import CreateView
# Create your views here.
from .models import Compare, Spell
from .forms import CompareForm, SpellCheckForm


class ComparePageView(MetadataMixin,JsonLdContextMixin, CreateView):
    form_class = CompareForm
    model = Compare
    title = 'Writing page'
    description = 'This is a compare page'

    template_name = "writing_tools/compare.html"

    structured_data = {
        "@type": "Organization",
        "name": "This is writing Company home",
        "description": _("A writing company."),
    }

    def get_structured_data(self):
        sd = super(ComparePageView, self).get_structured_data()
        return sd


class SpellCheckPageView(MetadataMixin,JsonLdContextMixin, CreateView):
    form_class = SpellCheckForm
    model = Spell
    title = 'Writing page'
    description = 'This is a compare page'

    template_name = "writing_tools/spell_check.html"

    structured_data = {
        "@type": "Organization",
        "name": "This is writing Company home",
        "description": _("A writing company."),
    }

    def get_structured_data(self):
        sd = super(SpellCheckPageView, self).get_structured_data()
        return sd
