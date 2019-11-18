from django.shortcuts import render
from samples.models import Sample
from django_json_ld.views import JsonLdDetailView
from django.views.generic.list import ListView
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin

# Create your views here.


class SampleListView(MetadataMixin, JsonLdContextMixin, ListView):
    model = Sample
    title = 'Professional Resume Writing Service | Desklib.com'
    use_title_tag = True
    description = 'Desklib provides you professional resume writing service. Your resume reflects who you are as a professional. Our team has created sample resumes for everyone who is looking for the perfect format for resume'
    keywords = ['professional resume writing service', 'resume writing services', 'resume services online', 'desklib resume writing service ']

    def get_context_data(self, **kwargs):
        context = super(SampleListView, self).get_context_data(**kwargs)
        context['resume_sample'] = Sample.objects.filter(type=1)
        return context


class SampleView(JsonLdDetailView):
    model = Sample






