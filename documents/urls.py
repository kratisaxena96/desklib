from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import DocumentView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps



urlpatterns = [

    path('<slug:slug>/', DocumentView.as_view(), name='document-view'),

]