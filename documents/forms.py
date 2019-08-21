from django import forms
from .models import Report


class reportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['issue', 'other_issue']