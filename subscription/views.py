from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_json_ld.views import JsonLdContextMixin
from meta.views import MetadataMixin
from .models import Download, PageView


class MyDownloads(MetadataMixin,JsonLdContextMixin,LoginRequiredMixin,TemplateView):
    template_name ="subscription/my_downloads.html"
    title = "My-Downloads"
    def get_context_data(self, **kwargs):
        context = super(MyDownloads, self).get_context_data(**kwargs)
        context['user_downloads'] = Download.objects.filter(user=self.request.user).order_by('created_at')
        context['page_view'] = PageView.objects.filter(user=self.request.user).order_by('created_at')
        return context
