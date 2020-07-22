from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import GenericSitemap
from subjects.models import Subject
from documents.models import Document
from homework_help.models import Question
from blogs.models import BlogModel
from samples.models import Sample
from django.urls import reverse
from django.utils import timezone


class SampleSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Sample.objects.filter(is_published=True, published_date__lte=timezone.now()).order_by('name')

    def lastmod(self, obj):
        return obj.published_date


class DocumentSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    limit = 20000

    def items(self):
        return Document.objects.filter(is_visible=True, is_published=True, published_date__lte=timezone.now()).only('published_date','slug')

    def lastmod(self, obj):
        return obj.published_date


class SubjectSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    # limit = 50000

    def items(self):
        return Subject.objects.filter(is_visible=True, updated__lte=timezone.now()).order_by('name')

    def lastmod(self, obj):
        return obj.updated


class QuestionSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    # limit = 50000

    def items(self):
        return Question.objects.filter(is_published=True, is_visible=True, published_date__lte=timezone.now()).order_by('question')

    def lastmod(self, obj):
        return obj.updated


class BlogSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    # limit = 50000

    def items(self):
        return BlogModel.objects.filter(is_published=True, is_visible=True, published_date__lte=timezone.now()).order_by('published_date')

    def lastmod(self, obj):
        return obj.updated


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about', 'contact', 'writing:writing', 'writing:compare', 'writing:grammar', 'homework_help:ask-question-view', 'blog']

    def location(self, item):
        return reverse(item)
