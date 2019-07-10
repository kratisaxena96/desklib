from django.views.generic import TemplateView, FormView
from .models import Document
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from meta.views import Meta
from django_json_ld.views import JsonLdContextMixin,settings,JsonLdSingleObjectMixin
from django.utils.translation import gettext as _
from haystack.generic_views import SearchMixin, SearchView
from meta.views import MetadataMixin
from django.views.generic.list import ListView


class DocumentView(TemplateView):
    template_name = "documents/document_template.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(DocumentView, self).get_context_data(*args, **kwargs)
        ctx['document'] = meta = Document.objects.filter(slug=self.kwargs['slug'])[0]
        ctx['meta'] = meta.as_meta(self.request)

        return ctx

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
