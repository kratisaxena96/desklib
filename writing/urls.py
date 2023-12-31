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

# from documents.views import HomePageView
from django.conf.urls.i18n import i18n_patterns
from .views import WritingPageView, ComparePageView, SpellCheckPageView, GrammarCorrectPageView
from samples.views import SampleListView, SampleView

urlpatterns = [
    path('', WritingPageView.as_view(), name="writing"),
    path('compare/', ComparePageView.as_view(), name="compare"),
    # path('grammar-checker/', SpellCheckPageView.as_view(), name="spell"),
    path('grammar-checker/', GrammarCorrectPageView.as_view(), name="grammar"),
    path('resume/', SampleListView.as_view(), name='sample-list-view'),
    path('resume/<slug:slug>/', SampleView.as_view(), name='sample-view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
