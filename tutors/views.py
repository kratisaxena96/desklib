from django.shortcuts import render

# Create your views here.
from django.utils.text import slugify
from django.views.generic import TemplateView, DetailView
from meta.views import MetadataMixin


from django_json_ld.views import JsonLdContextMixin
from homework_help.forms import QuestionHomeForm
from subjects.models import Subject
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect


class TutorPageView(MetadataMixin, JsonLdContextMixin, TemplateView):
    title = 'Desklib | Online Study Library'
    description = 'Get homework help fast! Desklib allows you to explore the best resources for your study ' \
                  'requirements. Search solutions, assignments, presentations, thesis, homework solutions from our' \
                  ' online learning library.'
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help']
    template_name = "tutor/v2/tutor.html"

    model = Subject
    form_class = QuestionHomeForm

    def get_context_data(self, **kwargs):
        context = super(TutorPageView, self).get_context_data(**kwargs)

        context['form'] = self.form_class
        return context

    def post(self,request):
        return redirect(reverse('tutors:tutor-list'))




class TutorListPageView(MetadataMixin, TemplateView):
    title = 'Desklib | Online Study Library'
    description = 'Get homework help fast! Desklib allows you to explore the best resources for your study requirements. Search solutions, assignments, presentations, thesis, homework solutions from our online learning library.'
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help']
    template_name = "tutor/v2/tutor_list.html"

class TutorDetailPageView(MetadataMixin, TemplateView):
    title = 'Desklib | Online Study Library'
    description = 'Get homework help fast! Desklib allows you to explore the best resources for your study requirements. Search solutions, assignments, presentations, thesis, homework solutions from our online learning library.'
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help']
    template_name = "tutor/v2/tutor_detail.html"

class TutorPlanPageView(MetadataMixin, TemplateView):
    title = 'Desklib | Online Study Library'
    description = 'Get homework help fast! Desklib allows you to explore the best resources for your study requirements. Search solutions, assignments, presentations, thesis, homework solutions from our online learning library.'
    keywords = ['homework writing services', 'online homework help', 'best online homework help website',
                'statistics homework help', 'engineering homework help', 'computer science homework help',
                'mechanical engineering homework help', 'humanities homework help', 'nursing homework help',
                'law homework help', 'tort law homework help', 'psychology homework help', '24 homework help',
                'urgent homework help']
    template_name = "tutor/v2/tutor_plans.html"

