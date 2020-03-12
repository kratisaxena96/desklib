from django import forms
from homework_help.models import Comment


class CommentForm(forms.ModelForm):
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder':"Enter first text to compare", 'class':"form-control"}), required=False)
    reference_files =forms.FileField(label='Reference Files', widget=forms.FileInput(attrs={'placeholder':"Enter first text to compare", 'class':"form-control", }), required=False)

    class Meta:
        model = Comment
        fields = ['message', 'reference_files']
