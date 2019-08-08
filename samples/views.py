from django.shortcuts import render
from samples.models import Sample
from django_json_ld.views import JsonLdDetailView
from django.views.generic.list import ListView

# Create your views here.
class SampleListView(ListView):
    model = Sample

    def get_context_data(self, **kwargs):
        context = super(SampleListView, self).get_context_data(**kwargs)
        context['resume_sample'] = Sample.objects.filter(type=1)
        return context


class SampleView(JsonLdDetailView):
    model = Sample






