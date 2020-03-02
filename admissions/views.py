from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django_json_ld.views import JsonLdContextMixin
from meta.views import MetadataMixin

from . forms import AspirantDetailsForm
from django.core.exceptions import SuspiciousOperation
from formtools.wizard.forms import ManagementForm

# Create your views here.
from .models import AspirantDetails

class AspirantDetailsView(CreateView):
    pass

from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import DefaultStorage

class ContactWizard(SessionWizardView):
    file_storage = DefaultStorage()


    def done(self, form_list, **kwargs):
        # form_list[1].country = form_list[0].country_code
        # AspirantDetails.objects.create(self.get_all_cleaned_data())
        m = AspirantDetails(**self.get_all_cleaned_data())
        m.save()
        return redirect('/')

    def get_context_data(self, form, **kwargs):
        context = super(ContactWizard, self).get_context_data(form, **kwargs)
        context['wizard'] = {
            'form': form,
            'steps': self.steps,
            'current_step': self.steps.current,
            'management_form': ManagementForm(prefix=self.prefix, initial={
                'current_step': self.steps.current,
            }),
        }
        return context

class AdmissionDetailView(MetadataMixin, JsonLdContextMixin, TemplateView):
    template_name = 'admissions/admission-details.html'
