from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from . views import AspirantDetailsView,ContactWizard, AdmissionDetailView
from .forms import AspirantDetailsForm, AspirantCountryDetailsForm, DesiredQualificationForm
from django.conf.urls import url

urlpatterns = [
    url(r'^contacts/$', ContactWizard.as_view([AspirantCountryDetailsForm, AspirantDetailsForm,DesiredQualificationForm]), name="multi-form"),
    path('admission-detail/', AdmissionDetailView.as_view(), name="admission-detail" )
    # path('', AspirantDetailsView.as_view(), name='aspirant'),

]
# urlpatterns += i18n_patterns(
#     path(r'^admissions/', ContactWizard.as_view([AspirantCountryDetailsForm, AspirantDetailsForm]), name='admissions')
# )
