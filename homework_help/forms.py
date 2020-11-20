from django import forms
from homework_help.models import Comment, Question, Order
from subjects.models import Subject
from django import forms
from haystack.forms import SearchForm
from django.contrib.admin import widgets


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
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder':"Enter your question here...", 'class':"form-control"}), required=False)
    reference_files =forms.FileField(label='Reference Files', widget=forms.FileInput(attrs={'placeholder':"Enter first text to compare", 'class':"form-control", }), required=False)

    class Meta:
        model = Comment
        fields = ['message', 'reference_files']



# class QuestionForm(forms.ModelForm):
#     question = forms.CharField(label='Question', widget=forms.Textarea(attrs={'placeholder':"Type Your Question here...", 'class': "form-design fade well", 'id': "dropzone", 'rows':14}), required=True)
#     subjects =forms.ModelChoiceField(empty_label='Eg. Maths, Science',queryset=Subject.objects.filter(is_parent=False), label='Subject', widget=forms.Select(attrs={'class':"form-field-design js-example-basic-multiple", }), required=True)
#     file =forms.FileField(label='Upload Files', widget=forms.FileInput(attrs={'class': "form-field-design", 'id': "fileupload", 'data-num':"1"}), required=False)
#     solution_deadline = forms.DateField(label='Deadline',
#         widget=widgets.AdminDateWidget(attrs={'type': 'date', 'placeholder': "Date", 'class': "form-field-design"}))
#
#
#     class Meta:
#         model = Question
#         fields = ['question', 'subjects', 'solution_deadline']

class QuestionForm(forms.ModelForm):
    question = forms.CharField(label='Question', widget=forms.Textarea(attrs={'placeholder':"Type Your Question here...", 'class': "form-control fade well", 'id': "dropzone", 'rows':10}), required=True)
    subjects =forms.ModelChoiceField(empty_label='Eg. Maths, Science',queryset=Subject.objects.filter(is_parent=False), label='Subject', widget=forms.Select(attrs={'class':"js-example-basic-multiple", }), required=True)
    file =forms.FileField(label='Upload Files', widget=forms.FileInput(attrs={'class': "", 'id': "fileupload", 'data-num':"1"}), required=False)
    solution_deadline = forms.DateField(label='Deadline',
        widget=widgets.AdminDateWidget(attrs={'type': 'date', 'placeholder': "Date", 'class': ""}))


    class Meta:
        model = Question
        fields = ['question', 'subjects', 'solution_deadline']


class QuestionHomeForm(forms.ModelForm):
    question = forms.CharField(label='Question', widget=forms.Textarea(attrs={'placeholder':"Type Your Question here...", 'class': "form-control rounded-0 ", 'id': "dropzone" ,'rows':"5"}), required=True)
    subjects =forms.ModelChoiceField(queryset=Subject.objects.filter(is_parent=False), label='Subject', widget=forms.Select(attrs={'class':"form-control js-example-basic-multiple border-radius-20", }), required=True)
    file =forms.FileField(label='Files', widget=forms.FileInput(attrs={'class': "form-control", 'id': "fileupload",'data-num':"1"}), required=False)


    class Meta:
        model = Question
        fields = ['question', 'subjects']


# class QuestionOrder(forms.Form):
#     is_consize =
#     is_detailed
