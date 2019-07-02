
from django import forms
from .models import Compare, Spell


class CompareForm(forms.ModelForm):
    textarea1 = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder':"Enter description about your requirement", 'class':"form-control d-block"}), required=False)
    textarea2= forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder':"Enter description about your requirement", 'class':"form-control d-block"}), required=False)

    class Meta:
        model = Compare
        fields = ['textarea1','textarea2']

class SpellCheckForm(forms.ModelForm):
    spell_textarea = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder':"Enter description about your requirement", 'class':"form-control", 'id':"mytextarea"}), required=False)

    class Meta:
        model = Spell
        fields = ['spell_textarea']