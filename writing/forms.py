
from django import forms


class CompareForm(forms.Form):
    textarea1 = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder':"Enter first text to compare", 'class':"form-control"}))
    textarea2= forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder':"Enter second text to compare", 'class':"form-control"}))

class SpellCheckForm(forms.Form):
    spell_textarea = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder':"Enter description about your requirement", 'class':"form-control", 'id':"mytextarea"}), required=False)
