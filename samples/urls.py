from django.urls import path, include
from .views import SampleView, SampleListView
from django.views.generic import TemplateView


urlpatterns = [
    path('', SampleListView.as_view(), name='sample-list-view'),
    path('resume/<slug:slug>/', SampleView.as_view(), name='sample-view'),

]