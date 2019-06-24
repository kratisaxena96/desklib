from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps import GenericSitemap
from .models import Document



class PostSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'


    def items(self):
        return Document.objects.filter(pk__lte =50000)

class PostSitemapTwo(Sitemap):
    priority = 0.5
    changefreq = 'daily'


    def items(self):
        return Document.objects.filter(pk__gte=50000,pk__lte=100000)

# all_sitemaps = {}
# for section in Document.objects.all():
#
#     info_dict = {
#         'queryset': section.article_set.filter(is_published=True),
#     }
#
#     sitemap = GenericSitemap(info_dict,priority=0.6)
#
#     # dict key is provided as 'section' in sitemap index view
#     all_sitemaps[section.name] = sitemap
#
