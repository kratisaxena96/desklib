from django import forms
from .models import Report, Issue
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class ReportForm(forms.ModelForm):
    issue = forms.ModelMultipleChoiceField(label='Issue', queryset=Issue.objects.all(), widget=forms.SelectMultiple(attrs={'class':"form-control", 'id':"id_issue"}), required=False)
    other_issue = forms.CharField(label='Comment', widget=forms.Textarea(attrs={'class':"form-control", 'id':"id_other_issue", 'rows':"3"}), required=False)

    class Meta:
        model = Report
        fields = ['issue', 'other_issue']


class DownloadFileForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    issue = forms.BooleanField(label='Agree to Terms and conditions', widget=forms.CheckboxInput(attrs={'class':"form-control", 'id': "id_issue"}))
