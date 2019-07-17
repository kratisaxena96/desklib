# some_app/views.py
from django.views.generic import TemplateView, DetailView,CreateView
from .models import Document
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


class DocumentView(JsonLdDetailView):
    model = Document

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        if request.user.is_anonymous:
            page_views = request.session.get('page_views')
            if page_views:
                if slug not in page_views:
                    page_views.append(slug)
                    request.session['page_views'] = page_views
                    # page_views.append(slug)
                    # print(page_views)
                else:
                    pass
            else:
                request.session['page_views']= [slug]

        else:
            self.object = self.get_object()
            PageView.objects.create(user=request.user, document=self.object)


        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            document_obj = Document.objects.get(slug=slug)
            download_obj = Download.objects.create(user=request.user, document=document_obj)
            # to-do
            attachments = {}
            pdf_doc_name = document_obj.pdf_converted_file.name.split('/')[-1]
            attachments[pdf_doc_name] = ContentFile(document_obj.pdf_converted_file.file.read())

            mail.send(
                request.user.email,  # List of email addresses also accepted
                settings.DEFAULT_FROM_EMAIL,
                subject='Your Download',
                message='Hi there!',
                html_message='Hi <strong>Here is your download</strong>!',
                attachments= attachments,
                priority= 'now'
            )
            return render(request, 'documents/document_detail.html')
        except Exception as e:
            print(e)





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


