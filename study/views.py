from django.views.generic.base import TemplateView

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.utils.highlighting import Highlighter
from django.views.generic import TemplateView, DetailView,CreateView
from documents.models import Document
from subscription.models import Download, PageView
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from django_json_ld.views import JsonLdDetailView
from django.views import View
from django.shortcuts import render
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from meta.views import Meta
from django_json_ld.views import JsonLdContextMixin,settings,JsonLdSingleObjectMixin
from django.utils.translation import gettext as _
from haystack.generic_views import SearchMixin, SearchView
from meta.views import MetadataMixin
from django.views.generic.list import ListView
from post_office import mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.files.base import ContentFile
import logging
from django_json_ld import settings
from haystack.forms import SearchForm

# Create your views here.

class StudyPageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Study page'
    description = 'This is a Study page'

    template_name = "study/study_list.html"

    structured_data = {
        "@type": "Organization",
        "name": "The Company home",
        "description": _("A Contact company."),
    }

    # def get(self, request, *args, **kwargs):
    #     recent = SearchQuerySet().order_by('-pub_date')[:5]
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(StudyPageView, self).get_context_data(**kwargs)
        recent = SearchQuerySet().order_by('-pub_date')[:5]
        # spellings = SearchQuerySet().spelling_suggestion('predident is goood')
        context['recent'] = recent
        # context['spellings'] = spellings

        return context

    def get_structured_data(self):
        sd = super(StudyPageView, self).get_structured_data()
        return sd

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')


class CustomSearchView(JsonLdContextMixin, MetadataMixin, SearchView):
    template_name = 'search/search.html'
    model = Document
    title = 'pashehi page'
    description = 'This is an sasassasaawesome page hey'
    keywords = ['Our', 'best', 'homepage']

    structured_data = {
        "@type": "Organizasaation",
        "name": "The Compasany home",
        "description": _("A greatesast hd company."),
    }

    def get_structured_data(self):
        sd = super(CustomSearchView, self).get_structured_data()
        return sd



