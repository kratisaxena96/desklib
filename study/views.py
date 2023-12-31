from django.db.models import Count

from documents.models import Document

import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django_json_ld.views import JsonLdContextMixin
from django.utils.translation import gettext as _
from haystack.generic_views import SearchView, FacetedSearchView
from meta.views import MetadataMixin
from subjects.models import Subject, SubjectContent
from .forms import CustomFacetedSearchForm


# Create your views here.

class StudyPageView(MetadataMixin, JsonLdContextMixin, SearchView):
    title = 'Desklib | Online Study Library'
    description = 'Get homework help fast! Desklib allows you to explore the best resources for your study requirements. Search solutions, assignments, presentations, thesis, homework solutions from our online learning library.'
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help']
    template_name = "study/v2/study_list.html"

    structured_data = {
        "@type": "Organization",
        "name": "desklib.com",
        "description": _(
            "Desklib allows you to explore best resources for your study requirements. Search solutions, assignments, presentations, thesis, homework solutions from our library."),
        "url": "https://desklib.com/study/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    # def get(self, request, *args, **kwargs):
    #     recent = SearchQuerySet().order_by('-pub_date')[:5]
    #     context = self.get_context_data(**kwargs)
    #     return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # sqs = SearchQuerySet().facet('subjects')
        # subjects = sqs.facet_counts()
        context = super(StudyPageView, self).get_context_data(**kwargs)
        recent = SearchQuerySet().order_by('-pub_date')[:5]
        top_results = SearchQuerySet().order_by('-views')[:5]
        # cover_image = top_results.pages.first().image_file.name
        context['top_results'] = top_results
        context['recent'] = recent
        doc = Subject.objects.annotate(doc_subject=Count('subject_documents'))
        context['doc_count'] = doc
        context['parent'] = Subject.objects.filter(parent_subject__isnull=True).prefetch_related('subject_set')
        # context['subject_facet'] = Subject.objects.all()
        return context

    def get_structured_data(self):
        sd = super(StudyPageView, self).get_structured_data()
        return sd


def autocomplete(request):
    # sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    sqs = SearchQuerySet().models(Document).filter(content_auto=request.GET.get('q', ''))[:5]
    # suggestions = [result.title for result in sqs]
    # slugs = [result.slug for result in sqs]
    # cover_imgage = [result.cover_image for result in sqs]
    # suggestions = dict(zip(titles, slugs))

    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    # the_data = json.dumps([{
    #     'results': suggestions,
    #     'slug':slugs,
    #     # 'cover_image': cover_imgage
    # }])
    data = {}
    item = {}
    i = 0
    # for i in range(len(sqs)):
    for result in sqs:
        document_obj = Document.objects.get(slug=result.slug)
        item["title"] = result.title
        item["slug"] = result.slug
        item["pages"] = result.no_of_pages
        try:
            words = document_obj.words
            item["words"] = words
        except:
            pass
        try:
            img = document_obj.pages.get(no=document_obj.cover_page_number).image_file
            item["image"] = img.url
        except:
            pass

        if len(result.description) > 250:
            item["description"] = (result.description[:250] + '..')
        else:
            item["description"] = data

        data[i] = item
        item = {}
        i += 1

    the_data = json.dumps(data)

    return HttpResponse(the_data, content_type='application/json')


class CustomSearchView(JsonLdContextMixin, MetadataMixin, FacetedSearchView):
    template_name = 'search/v2/search.html'
    model = Document
    queryset = SearchQuerySet().models(Document)
    form_class = CustomFacetedSearchForm
    facet_fields = ['subjects']
    paginate_by = 20
    title = 'Search Page | desklib.com'
    description = 'Search results for your query on desklib.com'
    keywords = ['Study resources', 'study notes search', 'study documents', 'study material search']
    suggestions = {}
    selected_facets = ['subjects', 'p_subject']
    # query_set =  None

    structured_data = {
        "@type": "Organizasaation",
        "name": "desklib.com",
        "description": _("Search results for your query on desklib.com"),
        "url": "https://desklib.com/study/search/",
        "logo": "https://desklib.com/static/dist/assets/images/desklib-logo-theme.png",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://www.desklib.com/study/search/?q={search_term}",
            "query-input": "required name=search_term"
        },
        "sameAs": [
            "https://www.facebook.com/desklib",
            "https://twitter.com/desklib",
            "https://www.linkedin.com/company/desklib",
            "https://www.instagram.com/desklib/"
        ]
    }

    def get_context_data(self, **kwargs):
        sqs = SearchQuerySet().facet('subjects')
        sqs_count = sqs.facet_counts()
        context = super(CustomSearchView, self).get_context_data(**kwargs)
        # context[settings.CONTEXT_ATTRIBUTE] = self.get_structured_data()
        # context['sqs'] = sqs_count
        slug_list = []
        for sub_filter in sqs_count.get('fields').get('subjects'):
            slug_list.append(sub_filter[0])
        context['slug_faceit'] = Subject.objects.filter(slug__in=slug_list)
        context['parent'] = Subject.objects.filter(parent_subject__isnull=True).prefetch_related('subject_set')
        context['subject_facet'] = Subject.objects.all()
        suggest_string = SearchQuerySet().spelling_suggestion(self.request.GET.get('q', ''))
        if self.request.GET.get('q', '') != suggest_string:
            context['suggestion'] = suggest_string
        context['selected'] = self.request.GET.get('selected_facets')
        if not self.request.GET.get('q') and not self.request.GET.get('selected_facets'):
            context['is_empty'] = True
        # context.update({'object_list': SearchQuerySet().filter(no_of_pages__range=[1, 5])})
        # self.searchqueryset = SearchQuerySet().order_by('-pub_date')[:5]

        # if self.suggestions:
        #     context['suggestion'] = self.suggestions
        # """Insert the form into the context dict."""
        # if 'form' not in kwargs:
        #     kwargs['form'] = self.get_form()
        return context

    # def get_queryset(self):
    #     queryset = super(CustomSearchView, self).get_queryset()
    #     # further filter queryset based on some set of criteria
    #     self.query_set = queryset
    #     return queryset

    def get_structured_data(self):
        sd = super(CustomSearchView, self).get_structured_data()
        return sd

    # def get(self, request, *args, **kwargs):
    #     # sqs = SearchQuerySet().filter(content=AutoQuery(request.GET['q']), subjects=Exact('sanskrit'))
    #     return super(CustomSearchView, self).get(request, *args, **kwargs)

# class FacetedSearchView(SearchView):
#     def extra_context(self):
#         extra = super(FacetedSearchView, self).extra_context()
#
#         if self.results == []:
#             extra['facets'] = self.form.search().facet_counts()
#         else:
#             extra['facets'] = self.results.facet_counts()
#
#         return extra
