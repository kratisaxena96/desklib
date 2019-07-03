from django.views.generic import TemplateView
from .models import Document
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet

class DocumentView(TemplateView):
    template_name = "documents/document_template.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(DocumentView, self).get_context_data(*args, **kwargs)
        ctx['slug'] = Document.objects.filter(slug=self.kwargs['slug'])
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