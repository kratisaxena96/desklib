# some_app/views.py
from django.views.generic import TemplateView
from .models import Document

class DcoumentView(TemplateView):
    template_name = "document_template.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(DcoumentView, self).get_context_data(*args, **kwargs)
        ctx['slug'] = Document.objects.filter(sul=self.kwargs['slug'])
        return ctx

