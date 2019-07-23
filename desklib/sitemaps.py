from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import GenericSitemap
from documents.models import Document
from django.urls import reverse
from django.utils import timezone

class DocumentSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'


    def items(self):
        return Document.objects.filter(is_published=True, published_date__lte=timezone.now()).order_by('id')

    def lastmod(self, obj):
        return obj.published_date

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home','about','contact']

    def location(self, item):
        return reverse(item)