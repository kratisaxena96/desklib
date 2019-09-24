from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_json_ld.views import JsonLdContextMixin
from meta.views import MetadataMixin
from .models import Download, PageView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class MyDownloads(MetadataMixin,JsonLdContextMixin,LoginRequiredMixin,TemplateView):
    template_name ="subscription/my_downloads.html"
    title = "My-Downloads"
    def get(self, request, *args, **kwargs):
        user_downloads = Download.objects.filter(user=self.request.user).order_by('created_at')
        paginator = Paginator(user_downloads, 6)
        page = request.GET.get('page1')
        try:
            user_downloads = paginator.page(page)
        except PageNotAnInteger:
            user_downloads = paginator.page(1)
        except EmptyPage:
            user_downloads = paginator.page(paginator.num_pages)

        page_view = PageView.objects.filter(user=self.request.user).order_by('created_at')
        paginator = Paginator(page_view, 6)
        page = request.GET.get('page2')
        try:
            page_view = paginator.page(page)
        except PageNotAnInteger:
            page_view = paginator.page(1)
        except EmptyPage:
            page_view = paginator.page(paginator.num_pages)

        context = {'user_downloads': user_downloads, 'page_view': page_view}

        return self.render_to_response(context)
