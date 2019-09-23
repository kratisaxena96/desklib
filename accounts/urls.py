from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import MyProfileView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps



urlpatterns = [
    path('', include('allauth.urls')),
    path('my-profile', MyProfileView.as_view(), name='my-profile'),
]
