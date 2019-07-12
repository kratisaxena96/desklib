from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView
from .views import StudyPageView
urlpatterns = [

    path('<slug:slug>/', StudyPageView.as_view(), name='study-detail'),
    path('', StudyPageView.as_view(), name='study-search'),

]