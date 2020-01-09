import os

from django import forms
from .models import AspirantDetails
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

COUNTRY = (
    ('uk', _('United Kingdom')),
    ('australia', _('Australia')),
)
QUALIFICATION = (
    ('under_grad', _('Under Graduate')),
    ('graduate', _('Graduate')),
    ('post_graduate', _('Post Graduate')),
    ('doctorate', _('Doctorate')),
)
STREAM = (
    ('arts', _('Arts')),
    ('science', _('Science')),
    ('tech', _('Technology')),
    ('commerce',_('Commerce'))
)
COURSES = (
    ('accounts', _('Accounting & Finance')),
    ('aeronautics', _('Aeronautical & Manufacturing Engineering')),
    ('agriculture', _('Agriculture & Forestry')),
    ('american', _('American Studies')),
    ('physiology', _('Anatomy & Physiology')),
    ('anthropology', _('Anthropology')),
    ('architecture', _('Architecture')),
    ('arts', _('Art & Design'))
)


class AspirantDetailsForm(forms.Form):
    name = forms.CharField(label=_('Name'), widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label=_('Email'), widget=forms.TextInput(attrs={'class': "form-control"}))
    phone = PhoneNumberField(label=_('Phone'), widget=forms.TextInput(attrs={'class': "form-control"}))
    qualification = forms.ChoiceField(label=_('Qualification'), choices=QUALIFICATION,
                                      widget=forms.Select(attrs={'class': "form-control  border-radius-20"}))
    stream = forms.ChoiceField(label=_('Stream'), choices=STREAM, widget=forms.Select(attrs={'class': "form-control "
                                                                                                      "border-radius-20"}))
    resume = forms.FileField(label=_('Upload Resume'), widget=forms.FileInput(attrs={'class': "form-control pt-1"}))

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        resume = cleaned_data.get("resume")
        if resume:
            ext = os.path.splitext(resume.name)[1]  # [0] returns path+filename
            valid_extensions = ['.pdf', '.doc', '.docx']
            if not ext.lower() in valid_extensions:
                raise forms.ValidationError('Unsupported file extension try to upload .pdf, .doc, .docx file types')

        if phone:
            if AspirantDetails.objects.filter(phone=phone):
                raise forms.ValidationError(
                    "This Phone no is already associated with another account Kindly Try again with another phone no."
                )


class AspirantCountryDetailsForm(forms.Form):
    country = forms.ChoiceField(label=_('Country'), widget=forms.RadioSelect, choices=COUNTRY)


class DesiredQualificationForm(forms.Form):
    lokking_for_stream = forms.ChoiceField(label=_('Stream Looking For'), choices=STREAM,
                                           widget=forms.Select(attrs={'class': "form-control border-radius-20"}))
    lokking_for_course = forms.ChoiceField(label=_('Course Looking For'), choices=COURSES,
                                           widget=forms.Select(attrs={'class': "form-control border-radius-20"}))
    year = forms.IntegerField()
