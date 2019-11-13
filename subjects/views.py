from django.shortcuts import render
from django.views.generic import TemplateView
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin

# Create your views here.


class SubjectsPageView(MetadataMixin, JsonLdContextMixin, TemplateView):
    template_name = "subjects/subject.html"
