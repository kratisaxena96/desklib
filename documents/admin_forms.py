from django.contrib.admin.widgets import AdminSplitDateTime
from django import forms
from accounts.models import UserAccount

class PublishedDateForm(forms.Form):
    date_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())

class ChangeAuthorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=UserAccount.objects.filter(is_staff=True, is_superuser=False))

    def __init__(self, user, *args, **kwargs):
        super(ChangeAuthorForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(
            queryset=UserAccount.objects.filter(is_staff=True, is_superuser=False,).exclude(username=user.username))
