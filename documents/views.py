# some_app/views.py
from django.views.generic import TemplateView, DetailView
from .models import Document

class DocumentView(DetailView):
    # template_name = "document_template.html"
    model = Document

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context





