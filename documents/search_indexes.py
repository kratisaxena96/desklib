from haystack import indexes
from .models import Document,Page
from haystack.query import SearchQuerySet
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from haystack.query import SearchQuerySet

# class search(SearchQuerySet):
#     sqs = SearchQuerySet().filter(content='foo').highlight()
#     import pdb; pdb.set_trace()
#     result = sqs[0]
#     result.highlighted['text'][0]  # u'Two computer scientists walk into a bar. The bartender says "<em>Foo</em>!".'

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
    cover_image = indexes.CharField()
    cover_image_name = indexes.CharField()
    no_of_pages = indexes.IntegerField(model_attr='page')
    no_of_words = indexes.IntegerField(model_attr='words')
    subjects = indexes.MultiValueField(faceted=True)
    views = indexes.CharField(model_attr='views')
    p_subject = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Document

    def prepare_content(self, obj):
        content = ' '.join(map(str, obj.content.split()[:500]))
        return content

    def prepare_subjects(self, obj):
        return [(t.slug) for t in obj.subjects.all()]

    def prepare_p_subject(self, obj):
        try:
            parent_sub = {(t.parent_subject.slug) for t in obj.subjects.all()}
        except:
            import pdb; pdb.set_trace()
        return list(parent_sub)

    def prepare_cover_image(self, obj):
        if obj.cover_page_number:
            url = obj.pages.get(no=obj.cover_page_number).image_file.url
            return url
        else:
            if obj.pages.count() >=2:
                # full_url = ''.join(['http://', get_current_site(obj).domain, obj.pages.first().image_file.url])
                url = obj.pages.all()[1].image_file.url
                # print(url)
                return url
            elif obj.pages.count() == 1:
                url = obj.pages.first().image_file.url
                return url

    def prepare_cover_image_name(self, obj):
        if obj.cover_page_number:
            name = obj.pages.get(no=obj.cover_page_number).image_file.name
            return name

        else:
            if obj.pages.count() >=2:
                # full_url = ''.join(['http://', get_current_site(obj).domain, obj.pages.first().image_file.url])
                name = obj.pages.all()[1].image_file.name
                # print(url)
                return name
            elif obj.pages.first():
                # full_url = ''.join(['http://', get_current_site(obj).domain, obj.pages.first().image_file.url])
                name = obj.pages.first().image_file.name
                # print(url)
                return name

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_visible=True, is_published=True, published_date__lte=timezone.now())


