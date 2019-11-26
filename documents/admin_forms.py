from django.contrib.admin.widgets import AdminSplitDateTime
from django import forms

class PublishedDateForm(forms.Form):
    date_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())