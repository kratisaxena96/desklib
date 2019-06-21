from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from django.urls import path, include
from .views import DcoumentView


sitemaps = {
'posts': PostSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('documents/<slug:slug>/', DcoumentView.as_view(), name='document'),

]