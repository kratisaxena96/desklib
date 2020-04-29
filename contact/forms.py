from django import forms
from contact.models import ContactUsModel


class ContactForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'placeholder': "Enter your name", 'class':"form-control"}), required=True)
    email = forms.CharField(label='Message', widget=forms.EmailField(attrs={'placeholder': "Enter your email", 'class':"form-control"}), required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'placeholder': "Enter your query", 'class':"form-control"}), required=True)

    class Meta:
        model = ContactUsModel
        fields = ['name', 'email', 'message']
