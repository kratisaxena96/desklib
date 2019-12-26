from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, FormView, ListView
from django_json_ld.views import JsonLdContextMixin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib import messages

from uploads.models import Upload
from uploads.forms import UploadForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from uploads.models import Upload

class UploadDocumentView(LoginRequiredMixin, JsonLdContextMixin, CreateView):
    form_class = UploadForm
    model = Upload
    template_name = 'uploads/upload_document.html'
    success_url = "/accounts/upload-file"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, 'Your form is being processed.')
        return super().form_valid(form)


class MyUploads(LoginRequiredMixin, ListView):
    model = Upload
    template_name = "uploads/my_uploads.html"
    paginate_by = 6
    title = "My-uploads"

    def get_queryset(self):
        queryset = super(MyUploads, self).get_queryset()
        queryset = queryset.filter(author=self.request.user).order_by('created')
        return queryset


    def get_context_data(self, **kwargs):
        context = super(MyUploads, self).get_context_data(**kwargs)
        upload = Upload.objects.filter(author=self.request.user).order_by('-created')
        paginator = Paginator(upload, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        context['object'] = file_exams
        return context