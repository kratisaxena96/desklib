from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import DocumentView, DocumentDownloadView, DownloadSuccessView, PageViewsFinishView, DocumentDownloadDetailView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps



urlpatterns = [
    path('<slug:slug>/', DocumentView.as_view(), name='document-view'),
    path('download/info/<slug:slug>/', DocumentDownloadDetailView.as_view(), name='download-info-view'),
    path('download/<slug:slug>/', DocumentDownloadView.as_view(), name='document-download-view'),
    path('download/success', DownloadSuccessView.as_view(), name='download-success-view'),
    path('extend/subscription', PageViewsFinishView.as_view(), name='pageviews-finish-view'),

]