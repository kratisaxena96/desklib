from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from .views import OrderDetailView
from django.views.generic import TemplateView
# from .sitemaps import all_sitemaps as sitemaps


urlpatterns = [
    path('<order_id>/', OrderDetailView.as_view(), name='download-info-view'),
]

