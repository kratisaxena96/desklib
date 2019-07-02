# some_app/views.py
from django.views.generic import TemplateView, DetailView
from .models import Document

class DocumentView(DetailView):
    # template_name = "document_template.html"
    model = Document

