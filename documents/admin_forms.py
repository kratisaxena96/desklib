from django.contrib.admin.widgets import AdminSplitDateTime
from django import forms
from accounts.models import UserAccount
from documents.models import Document
from datetime import datetime


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

    def __init__(self, *args, **kwargs):
        super(DocumentAdminForm, self).__init__(*args, **kwargs)
        is_published = self.initial.get('is_published')
        is_visible = self.initial.get('is_visible')
        published_date = self.initial.get("published_date")
        # date = str(published_date.day) + "/" + str(published_date.month) + "/" + str(published_date.year)
        # today_date = str(datetime.today().day) + "/" + str(datetime.today().month) + "/" + str(datetime.today().year)

        if is_published and is_visible:
            # self.fields['slug'] = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
            self.fields['slug'].widget.attrs['readonly'] = True

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
