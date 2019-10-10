from django import forms
from django_countries.fields import CountryField
from uploads.models import Upload
from django_countries.widgets import CountrySelectWidget
from subjects.models import Subject
from django.db.models import Q

class UploadForm(forms.ModelForm):
    course_name = forms.CharField(label='Course Name', widget=forms.TextInput(attrs={'class': "form-control form-rounded", 'placeholder':"Course Name...",}))
    # subjects = forms.ChoiceField(label='Subject',initial=0, widget=forms.Select(attrs={'class': "form-control"}), required=True)
    subjects = forms.ModelMultipleChoiceField(queryset= Subject.objects.filter(~Q(parent_subject=None)), initial=0, widget=forms.SelectMultiple(attrs={'class': "form-control js-example-basic-multiple"}))

    type = forms.ChoiceField(label='Type of Document', choices=Upload.TYPE_OF_DOCUMENT, widget=forms.Select(attrs={'class': "form-control form-rounded"}))
    upload_file = forms.FileField(label='Upload Document', widget=forms.FileInput(attrs={'class': "form-control custom-file-input", 'id': "inputGroupFile02"}))
    course_code = forms.CharField(label='Course Code', widget=forms.TextInput(attrs={'class': "form-control form-rounded", 'placeholder':"Course Code..."}))
    country = CountryField().formfield(blank_label='(select country)', widget=CountrySelectWidget(attrs={'class': "form-control js-example-basic-single"}))
    university = forms.CharField(label='University', widget=forms.TextInput(attrs={'class': "form-control form-rounded", 'placeholder':"Your University"}))

    class Meta:
        model = Upload
        fields = ['course_name', 'course_code','upload_file','country', 'university', 'type','subjects']

        # def __init__(self, *args, **kwargs):
        #     super(UploadForm, self).__init__(*args, **kwargs)
        #     self.fields['subjects'].queryset = Subject.objects.filter(~Q(parent_subject=None))
