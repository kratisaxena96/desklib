from django.contrib.admin.widgets import AdminSplitDateTime
from django import forms
from accounts.models import UserAccount
from documents.models import Document


class PublishedDateForm(forms.Form):
    date_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())

class ChangeAuthorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=UserAccount.objects.filter(is_staff=True, is_superuser=False))

    def __init__(self, user, *args, **kwargs):
        super(ChangeAuthorForm, self).__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(
            queryset=UserAccount.objects.filter(is_staff=True, is_superuser=False,).exclude(username=user.username))

class DocumentAdminForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude = ()

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title:
            qs = Document.objects.filter(title=title)
            if qs:
                if self.instance.pk is not None:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    raise forms.ValidationError(
                        "This Title is already associated with another Document Kindly Try again with another Title."
                    )
            if len(title) < 24:
                raise forms.ValidationError(
                    "Title should be greater than 30 characters"
                )
