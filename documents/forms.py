from django import forms
from .models import Report, Issue


class reportForm(forms.ModelForm):
    issue = forms.ModelMultipleChoiceField(label='Issue', queryset=Issue.objects.all(), widget=forms.SelectMultiple(attrs={'class':"form-control", 'id':"id_issue"}), required=False)
    other_issue = forms.CharField(label='Comment', widget=forms.Textarea(attrs={'class':"form-control", 'id':"id_other_issue"}), required=False)

    class Meta:
        model = Report
        fields = ['issue', 'other_issue']