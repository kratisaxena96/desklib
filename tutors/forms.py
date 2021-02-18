from django import forms
# from .models import Tutor
#
#
# class TestForm(forms.Form):
#
#     class Meta:
#         model = Tutor
#         fields = "__all__"
from subjects.models import Subject


# class NamesChoiceField(ModelMultipleChoiceField):
#
#

class TutorSubjectForm(forms.ModelForm):

    recipient = forms.ModelChoiceField(queryset=Subject.objects.all(), required=True)

    class Meta:
        model = Subject
        fields = [
            'recipient'
        ]

    # def init(self, args, kwargs):
    #
    #     task = kwargs.pop('recipient', None)
    #     super(TutorSubjectForm, self).__init__(args, kwargs)
    #     queries = []
    #
