from django import forms
from django_countries.fields import CountryField
from uploads.models import Upload
from django_countries.widgets import CountrySelectWidget

class UploadForm(forms.ModelForm):
    course_name = forms.CharField(label='Course Name', widget=forms.TextInput(attrs={'class': "form-control"}), required=True)
    # subjects = forms.ChoiceField(label='Subject', choices=Subject, widget=forms.Select(attrs={'class': "form-control"}), required=True)
    type = forms.ChoiceField(label='Type of Document', choices=Upload.TYPE_OF_DOCUMENT, widget=forms.Select(attrs={'class': "form-control"}), required=True)
    upload_file = forms.FileField(label='Upload Document', widget=forms.FileInput(attrs={'class': "form-control"}), required=True)
    course_code = forms.CharField(label='Course Code', widget=forms.TextInput(attrs={'class': "form-control"}), required=False)
    country = CountryField().formfield(blank_label='(select country)', widget=CountrySelectWidget(attrs={'class': "form-control"}))
    university = forms.CharField(label='University', widget=forms.TextInput(attrs={'class': "form-control"}), required=False)

    class Meta:
        model = Upload
        fields = ['course_name', 'course_code', 'country', 'university', 'type', 'upload_file', 'subjects']