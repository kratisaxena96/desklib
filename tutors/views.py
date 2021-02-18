# Create your views here.
from django.http.response import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, DetailView
from meta.views import MetadataMixin

from django_json_ld.views import JsonLdContextMixin
from homework_help.forms import QuestionHomeForm
from subjects.models import Subject
from django.urls import reverse
from django.shortcuts import redirect
from .models import Tutor
from django.contrib import messages


# def post(self, request):
#     sub = request.POST['subjects'] if request.POST['subjects'] else None
#     sub = Subject.objects.get(id=sub)
#     print(Tutor.objects.filter(subjects__slug=sub).exists())
#     if Tutor.objects.filter(subjects__slug=sub).exists():
#         if sub is not None:
#             messages.success(request, "there is your tutor list")
#             return redirect('{0}?{1}'.format(reverse('tutors:tutor-list'), sub.slug))
#     else:
#         messages.error(request, "No tutors found in this subject")
#         return HttpResponseRedirect(reverse('tutors:tutor'))


class TutorPageView(MetadataMixin, JsonLdContextMixin, TemplateView):
    title = 'Desklib | Online Study Library'
    description = """
            Get homework help fast! Desklib allows you to explore the best resources for your study 
            requirements. Search solutions, assignments, presentations, thesis, homework solutions from our
            online learning library.
        """
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help'
                ]
    template_name = "tutor/v2/tutor.html"
    model = Subject
    form_class = QuestionHomeForm

    def get_context_data(self, **kwargs):
        context = super(TutorPageView, self).get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def post(self, request):
        sub = request.POST['subjects'] if request.POST['subjects'] else None
        sub = Subject.objects.get(id=sub)
        if Tutor.objects.filter(subjects__slug=sub.slug).exists():
            if sub is not None:
                messages.success(request, "there is your tutor list")
                return redirect('{0}?{1}'.format(reverse('tutors:tutor-list'), sub.slug))
        else:
            messages.error(request, "No tutors found in this subject")
            return HttpResponseRedirect(reverse('tutors:tutor'))


class TutorListPageView(MetadataMixin, ListView):
    title = 'Desklib | Online Study Library'
    description = """
            Get homework help fast! Desklib allows you to explore the best 
            resources for your study requirements. Search solutions, assignments, 
            presentations, thesis, homework solutions from our online learning library.
        """
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help'
                ]
    template_name = "tutor/v2/tutor_list.html"

    model = Tutor
    slug_field = 'slug'
    slug_url_kwargs = 'slug'
    queryset = Tutor.objects.all()

    def get_queryset(self):
        data = self.request.get_full_path()
        queryset = super(TutorListPageView, self).get_queryset()
        queryset = queryset.filter(subjects__slug=data[19:])
        return queryset


class TutorDetailPageView(MetadataMixin, DetailView):
    title = 'Desklib | Online Study Library'
    description = """
        Get homework help fast! Desklib allows you to explore the 
        best resources for your study requirements. Search solutions, 
        assignments, presentations, thesis, homework solutions from our online learning library.
    """

    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help'
                ]
    template_name = "tutor/v2/tutor_detail.html"
    model = Tutor

    def get_object(self, queryset=None):
        return Tutor.objects.get(slug=self.kwargs.get("slug"))


class TutorPlanPageView(MetadataMixin, TemplateView):
    title = 'Desklib | Online Study Library'
    description = """Get homework help fast! Desklib allows you to explore the best 
                resources for your study requirements. Search solutions, assignments, 
                presentations, thesis, homework solutions from our online learning library.
                """
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help']
    template_name = "tutor/v2/tutor_plans.html"

