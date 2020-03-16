from django import forms
from homework_help.models import Comment, Question
from subjects.models import Subject


class CommentForm(forms.ModelForm):
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder':"Enter your question here...", 'class':"form-control"}), required=False)
    reference_files =forms.FileField(label='Reference Files', widget=forms.FileInput(attrs={'placeholder':"Enter first text to compare", 'class':"form-control", }), required=False)

    class Meta:
        model = Comment
        fields = ['message', 'reference_files']


class QuestionForm(forms.ModelForm):
    question = forms.CharField(label='Question', widget=forms.Textarea(attrs={'placeholder':"Type Your Question here...", 'class': "form-control rounded-0 fade well", 'id': "dropzone"}), required=True)
    subjects =forms.ModelChoiceField(queryset=Subject.objects.filter(is_parent=False), label='Subject', widget=forms.Select(attrs={'placeholder':"Enter first text to compare", 'class':"form-control border-radius-20", }), required=True)
    file =forms.FileField(label='Files', widget=forms.FileInput(attrs={'placeholder': "Enter first text to compare", 'class': "form-control", 'id': "fileupload"}), required=False)


    class Meta:
        model = Question
        fields = ['question', 'subjects']
