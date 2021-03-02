from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from subscription.utils import get_current_subscription


class MyProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/my_profile.html'

    def get_context_data(self, **kwargs):
        context = super(MyProfileView, self).get_context_data(**kwargs)
        user_obj = self.request.user
        subscription_obj = get_current_subscription(self.request.user)
        context['user'] = user_obj
        context['subscription'] = subscription_obj
        return context
