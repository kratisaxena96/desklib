from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django_json_ld.views import JsonLdContextMixin
from meta.views import MetadataMixin
from review.models import Review


class ReviewPageView(MetadataMixin, JsonLdContextMixin, ListView):
    template_name = "review/review.html"
    model = Review

    def get_context_data(self, **kwargs):
        context = super(ReviewPageView, self).get_context_data(**kwargs)
        return context
