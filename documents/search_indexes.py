from haystack import indexes
from .models import Document
from haystack.query import SearchQuerySet
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.views.generic.base import TemplateView
from django.utils import timezone
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


    keywords = ['Our', 'best', 'homepage']
    twitter_title = 'Hello Twitter'

    # authors = indexes.CharField()
    def get_model(self):
        return Document
    # def prepare_authors(self, obj):
    #     return [ a.name for a in obj.author.all()]
    def index_queryset(self, using=None):
        return self.get_model().objects.all()


