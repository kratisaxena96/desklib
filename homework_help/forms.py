from django import forms
from homework_help.models import Comment, Question
from subjects.models import Subject
from django import forms
from haystack.forms import SearchForm


class QuestionSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super(QuestionSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs



class CommentForm(forms.ModelForm):
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder':"Enter your message", 'class':"form-control"}), required=False)
    reference_files =forms.FileField(label='Reference Files', widget=forms.FileInput(attrs={'placeholder':"Enter first text to compare", 'class':"form-control", }), required=False)

    class Meta:
        model = Comment
        fields = ['message', 'reference_files']


class QuestionForm(forms.ModelForm):
    question = forms.CharField(label='Question', widget=forms.Textarea(attrs={'placeholder':"", 'class': "form-control fade well", 'id': "dropzone"}), required=True)
    subjects =forms.ModelChoiceField(queryset=Subject.objects.filter(is_parent=False), label='Subject', widget=forms.Select(attrs={'placeholder':"Enter first text to compare", 'class':"form-control", }), required=True)
    file =forms.FileField(label='Files', widget=forms.FileInput(attrs={'placeholder': "Enter first text to compare", 'class': "form-control", 'id': "fileupload"}), required=False)


    class Meta:
        model = Question
        fields = ['question', 'subjects']
