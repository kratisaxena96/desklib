# some_app/views.py
from django.views.generic import TemplateView, DetailView,CreateView
from .models import Document
from subscription.models import Download
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


class DocumentView(LoginRequiredMixin, JsonLdDetailView):
    model = Document

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            document_obj = Document.objects.get(slug=slug)
            download_obj = Download.objects.create(user=request.user, document=document_obj)
            # to-do
            mail.send(
                settings.DEFAULT_FROM_EMAIL,  # List of email addresses also accepted
                settings.DEFAULT_FROM_EMAIL,
                subject='My email',
                message='Hi there!',
                html_message='Hi <strong>there</strong>!',
            )
        except Exception as e:
            print(e)

        return render(request, 'documents/document_detail.html')




        # download_add = Download.objects.create(document , user)

        # return render(request, 'documents/document_detail.html')

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context


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


    # def get_context_data(self, **kwargs):
    #     context = super(JsonLdContextMixin, self).get_context_data(**kwargs)
    #     context[settings.CONTEXT_ATTRIBUTE] = self.get_structured_data()
    #     context['xyz'] = "rishis"
    #     # return context
    #     """Insert the form into the context dict."""
    #     if 'form' not in kwargs:
    #         kwargs['form'] = self.get_form()
    #     return context
