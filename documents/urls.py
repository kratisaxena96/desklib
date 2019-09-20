from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import DocumentView, DocumentDownloadView, DownloadSuccessView, PageViewsFinishView, DocumentDownloadDetailView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps



urlpatterns = [
    path('download/confirm/', DocumentDownloadDetailView.as_view(), name='download-info-view'),
    path('download/', DocumentDownloadView.as_view(url='https://desklib.com/?doc=%(slug)'), name='document-download-view'),
    path('download/success', DownloadSuccessView.as_view(), name='download-success-view'),
    path('extend/subscription', PageViewsFinishView.as_view(), name='pageviews-finish-view'),
    path('<slug:slug>/', DocumentView.as_view(), name='document-view'),
]
