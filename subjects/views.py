from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from haystack.query import SearchQuerySet
from meta.views import MetadataMixin
from django_json_ld.views import JsonLdContextMixin

# Create your views here.
from homework_help.models import Question
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


        all = SearchQuerySet().filter(p_subject=parent_subject)[:20]
        recent = SearchQuerySet().filter(p_subject=parent_subject).order_by('-pub_date')[:20]
        top_results = SearchQuerySet().filter(p_subject=parent_subject).order_by('-views')[:20]
        # print(doc[0].doc_subject)

        question = Question.objects.filter(subjects=parent_subject.id)

        for i in child_subject:
            ques = Question.objects.filter(subjects=i.id)
            question = question | ques

        question = question.order_by('-published_date')[:5]

        context['meta'] = self.get_object().as_meta(self.request)
        context['child_subject'] = child_subject
        context['document'] = document
        context['recent'] = recent
        context['top_results'] = top_results
        context['doc_count'] = doc
        context['question'] = question
        return context


class ChildSubjectPageView(MetadataMixin, JsonLdContextMixin, DetailView):
    template_name = "subjects/child_subject.html"
    model = Subject

    def get_context_data(self, **kwargs):
        context = super(ChildSubjectPageView, self).get_context_data(**kwargs)
        child_subject = Subject.objects.get(slug=self.kwargs['slug'])
        recent = SearchQuerySet().filter(subjects=child_subject).order_by('-pub_date')[:20]
        top_results = SearchQuerySet().filter(subjects=child_subject).order_by('-views')[:20]

        question = Question.objects.filter(subjects=child_subject.id).order_by('-published_date')[:5]

        # context['child'] = child_subject
        context['meta'] = self.get_object().as_meta(self.request)
        context['document'] = Document.objects.filter(subjects=child_subject.id)
        context['recent'] = recent
        context['top_results'] = top_results
        context['question'] = question
        return context
