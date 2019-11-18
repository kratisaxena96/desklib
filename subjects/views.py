from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin

# Create your views here.
from subjects.models import Subject
from documents.models import Document
from django.db.models import Count


class SubjectsPageView(MetadataMixin, JsonLdContextMixin, ListView):
    template_name = "subjects/subject.html"
    model = Subject


    def get_context_data(self, **kwargs):
        context = super(SubjectsPageView, self).get_context_data(**kwargs)
        doc = Subject.objects.annotate(doc_subject=Count('subject_documents'))

        context['doc_count'] = doc
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(SubjectsPageView, self).get_context_data(**kwargs)
    #     context['parent_subject'] = Subject.objects.filter(parent_subject__isnull=True).prefetch_related('subject_set')
    #     context['child_subject'] = Subject.objects.all()
    #     return context


class ParentSubjectPageView(MetadataMixin, JsonLdContextMixin, DetailView):
    template_name = "subjects/parent_subject.html"
    model = Subject

    def get_context_data(self, **kwargs):
        context = super(ParentSubjectPageView, self).get_context_data(**kwargs)
        parent_subject = Subject.objects.get(slug=self.kwargs['slug'])
        child_subject = Subject.objects.filter(parent_subject=parent_subject.id)
        document = Document.objects.filter(subjects=parent_subject.id)
        doc = Subject.objects.filter(parent_subject=parent_subject.id).annotate(doc_subject=Count('subject_documents'))
        # print(doc[0].doc_subject)

        context['child_subject'] = child_subject
        context['document'] = document
        context['doc_count'] = doc
        return context


class ChildSubjectPageView(MetadataMixin, JsonLdContextMixin, DetailView):
    template_name = "subjects/child_subject.html"
    model = Subject

    def get_context_data(self, **kwargs):
        context = super(ChildSubjectPageView, self).get_context_data(**kwargs)
        child_subject = Subject.objects.get(slug=self.kwargs['slug'])
        # context['child'] = child_subject
        context['document'] = Document.objects.filter(subjects=child_subject.id)
        return context
