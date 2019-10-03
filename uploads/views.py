from django.shortcuts import render
from django.views.generic import CreateView
from uploads.models import Upload
from uploads.forms import UploadForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class UploadDocumentView(LoginRequiredMixin, CreateView):
    form_class = UploadForm
    model = Upload
    template_name = 'uploads/upload_document.html'
