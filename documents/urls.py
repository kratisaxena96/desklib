from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap,PostSitemapTwo
from django.urls import path, include
from .views import DcoumentView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps



sitemaps = {
'post': PostSitemap,

}
sitemaps2 = {
'post': PostSitemapTwo,
}
# urlpatterns += patterns('',
#         (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
#         (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
# )

urlpatterns = [

    path('sitemap1.xml', sitemap, {'sitemaps': sitemaps},
         name='sitemap1'),
    path('sitemap2.xml', sitemap, {'sitemaps': sitemaps2},
         name='sitemap2'),
    path('<slug:slug>/', DcoumentView.as_view(), name='document-view'),
    path('sitemap-index.xml/',TemplateView.as_view(template_name='documents/sitemap-index.xml',content_type='text/xml'), name='sitemap_index'),

]