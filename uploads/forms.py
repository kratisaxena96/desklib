from django import forms
from django_countries.fields import CountryField
from uploads.models import Upload
from django_countries.widgets import CountrySelectWidget
from subjects.models import Subject
from django.db.models import Q
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 5242880

class UploadForm(forms.ModelForm):
    course_name = forms.CharField(label='Course Name', widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Course Name...",}), )
    # subjects = forms.ChoiceField(label='Subject',initial=0, widget=forms.Select(attrs={'class': "form-control"}), required=True)
    subjects = forms.ModelMultipleChoiceField(queryset= Subject.objects.filter(~Q(parent_subject=None)), initial=0, widget=forms.Select(attrs={'class': "form-control js-example-basic-multiple", 'multiple': "multiple"}))

    type = forms.ChoiceField(label='Type of Document', choices=Upload.TYPE_OF_DOCUMENT, widget=forms.Select(attrs={'class': "form-control"}))
    upload_file = forms.FileField(label='Upload Document', widget=forms.FileInput(attrs={'class': "form-control custom-file-input"}), required=True)
    course_code = forms.CharField(label='Course Code', widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Course Code..."}), required=False)
    country = CountryField().formfield(blank_label='(select country)', widget=CountrySelectWidget(attrs={'class': "form-control js-example-basic-single"}))
    university = forms.CharField(label='University', widget=forms.TextInput(attrs={'class': "form-control", 'placeholder':"Your University"}), required=False)

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