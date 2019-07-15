from django.views.generic.base import TemplateView

from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.utils.highlighting import Highlighter

# Create your views here.

class StudyPageView(MetadataMixin,JsonLdContextMixin, TemplateView):
    title = 'Study page'
    description = 'This is a Study page'

    template_name = "study/study.html"

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
        context['recent'] = recent
        return context

    def get_structured_data(self):
        sd = super(StudyPageView, self).get_structured_data()
        return sd
