from django.contrib.sitemaps import Sitemap
from .models import Document

class PostSitemap(Sitemap):

    def items(self):
        return Document.objects.all()