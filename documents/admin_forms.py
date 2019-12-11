from django.contrib.admin.widgets import AdminSplitDateTime
from django import forms
from accounts.models import UserAccount

class PublishedDateForm(forms.Form):
    date_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())

class ChangeAuthorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=UserAccount.objects.filter(is_staff=True, is_superuser=False))


