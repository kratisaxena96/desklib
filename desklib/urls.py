"""desklib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from .sitemaps import DocumentSitemap,StaticViewSitemap
from django.contrib.sitemaps import views
from .views import HomePageView, AboutPageView, PricingPageView, ContactPageView, TestPageView
if settings.DEBUG:
    import debug_toolbar
from documents.views import autocomplete,CustomSearchView

sitemaps = {
    'documents': DocumentSitemap,
    'static':StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),  # new
    path('accounts/', include('allauth.urls')),
    path('study/',include(('study.urls','study'),namespace="study")),
    path('', HomePageView.as_view(), name='home'),
    path('document/', include(('documents.urls','documents'),namespace="documents")),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('pricing/', PricingPageView.as_view(), name='pricing'),
    path('test/', TestPageView.as_view(), name='test'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('search/', CustomSearchView.as_view(),),
    path(r'autocomplete/', autocomplete, name='autocomplete'),
    path('writing/', include(('writing.urls', 'writing'), namespace="writing")),
    path('robots.txt/', include('robots.urls')),
    path('sitemap.xml/', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^$', HomePageView.as_view(), name='home'),
    # url(r'^admin/', include(admin.site.urls)),
)


handler404 = 'desklib.views.handler404'
handler500 = 'desklib.views.handler500'