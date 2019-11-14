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
from .views import SubjectsPageView, ParentSubjectPageView, ChildSubjectPageView
from samples.views import SampleListView, SampleView

urlpatterns = [
    path('', SubjectsPageView.as_view(), name="subjects"),
    path('<slug:parent_subject>/<slug:slug>/', ChildSubjectPageView.as_view(), name='child-subject-view'),
    path('<slug:slug>/', ParentSubjectPageView.as_view(), name='parent-subject-view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
