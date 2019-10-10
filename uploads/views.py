from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, FormView, ListView
from django_json_ld.views import JsonLdContextMixin

from uploads.models import Upload
from uploads.forms import UploadForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from uploads.models import Upload

class UploadDocumentView(LoginRequiredMixin, JsonLdContextMixin, CreateView):
    form_class = UploadForm
    model = Upload
    template_name = 'uploads/upload_document.html'
    success_url = "/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class MyUploads(LoginRequiredMixin, ListView):
    model = Upload
    template_name = "uploads/my_uploads.html"
    paginate_by = 2
    title = "My-uploads"

    def get_queryset(self):
        queryset = super(MyUploads, self).get_queryset()
        queryset = queryset.filter(author=self.request.user).order_by('created')
        return queryset
