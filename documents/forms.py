from django import forms

from subjects.models import Subject
from .models import Report, Issue
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django_countries.fields import CountryField
from uploads.models import Upload
from django_countries.widgets import CountrySelectWidget
from django.db.models import Q
from django.template.defaultfilters import filesizeformat

class ReportForm(forms.ModelForm):
    issue = forms.ModelMultipleChoiceField(label='Issue', queryset=Issue.objects.all(), widget=forms.SelectMultiple(attrs={'class':"form-control", 'id':"id_issue"}), required=False)
    other_issue = forms.CharField(label='Comment', widget=forms.Textarea(attrs={'class':"form-control", 'id':"id_other_issue", 'rows':"3"}), required=False)

    class Meta:
        model = Report
        fields = ['issue', 'other_issue']


class DownloadFileForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    issue = forms.BooleanField(label='Agree to Terms and conditions', widget=forms.CheckboxInput(attrs={'id': "id_issue"}))
    file = forms.CharField(label='slug', widget=forms.HiddenInput(attrs={'class': "form-control"}), required=False)


# class UploadFileForm(forms.ModelForm):
#     upload_file =forms.FileField(label='Files', widget=forms.FileInput(attrs={'class': "form-control", 'id': "fileupload"}))
#
#     class Meta:
#         model = Upload
#         fields = ['upload_file', 'course_name', 'subjects', 'type']



MAX_UPLOAD_SIZE = 5242880

class UploadFileForm(forms.ModelForm):
    course_name = forms.CharField(label='Course Name', widget=forms.TextInput(attrs={'class': "form-control form-rounded", 'placeholder':"Course Name...", 'id': "id_course_name2"}))
    # subjects = forms.ChoiceField(label='Subject',initial=0, widget=forms.Select(attrs={'class': "form-control"}), required=True)
    subjects = forms.ModelMultipleChoiceField(queryset= Subject.objects.filter(~Q(parent_subject=None)), initial=0, widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple", 'id': "id_subjects_2"}))

    type = forms.ChoiceField(label='Type of Document', choices=Upload.TYPE_OF_DOCUMENT, widget=forms.Select(attrs={'class': "form-control form-rounded", 'id': "id_type_2"}))
    upload_file = forms.FileField(label='Upload Document', widget=forms.FileInput(attrs={'class': "form-control custom-file-input", 'id': "inputGroupFile02_2"}))
    course_code = forms.CharField(label='Course Code', widget=forms.TextInput(attrs={'class': "form-control form-rounded", 'placeholder':"Course Code...", 'id': "id_course_code_2"}), required=False)
    country = CountryField().formfield(blank_label='(select country)', widget=CountrySelectWidget(attrs={'class': "form-control js-example-basic-single", 'id': "id_country_2"}))
    university = forms.CharField(label='University', widget=forms.TextInput(attrs={'class': "form-control form-rounded", 'placeholder':"Your University", 'id': "id_university_2"}), required=False)

    class Meta:
        model = Upload
        fields = ['course_name', 'course_code','upload_file','country', 'university', 'type','subjects']

        # def __init__(self, *args, **kwargs):
        #     super(UploadForm, self).__init__(*args, **kwargs)
        #     self.fields['subjects'].queryset = Subject.objects.filter(~Q(parent_subject=None))
    def clean_upload_file(self):
        content = self.cleaned_data['upload_file']
        if content.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content.size)))
        return content
