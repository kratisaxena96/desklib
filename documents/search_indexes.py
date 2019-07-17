from haystack import indexes
from .models import Document,Page
from haystack.query import SearchQuerySet
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site


import pytz

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/book_text.txt")
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    content = indexes.CharField(model_attr='content')
    summary = indexes.CharField(model_attr='summary')
    content_auto = indexes.EdgeNgramField(model_attr='description')
    slug = indexes.CharField(model_attr='slug')
    pub_date = indexes.DateTimeField(model_attr='published_date')
    authors = indexes.CharField()

    def get_model(self):
        return Document

    def prepare_authors(self, obj):
        if  obj.pages.first():
            # import pdb; pdb.set_trace()
            # full_url = ''.join(['http://', get_current_site(obj).domain, obj.pages.first().image_file.url])

            # return  "%s" % (full_url)
            return  "%s" % (obj.pages.first().image_file.url)

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(published_date__lte=timezone.now())


