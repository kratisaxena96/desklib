from allauth.account.forms import SignupForm
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from phonenumber_field.formfields import PhoneNumberField

class CustomSignupForm(SignupForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV3,label=False)

    first_name = forms.CharField(max_length=40, label='First Name', widget=forms.TextInput(attrs={'placeholder':"First Name",'class':"form-control"}))
    last_name = forms.CharField(max_length=40, label='Last Name', widget=forms.TextInput(attrs={'placeholder':"Last Name",'class':"form-control"}))
    contact_no = PhoneNumberField(max_length=20, label='Contact No', widget=forms.TextInput(attrs={'placeholder':"e.g. +91-9876543210",'class':"form-control"}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.contact_no = self.cleaned_data['contact_no']
        user.save()
        return user
