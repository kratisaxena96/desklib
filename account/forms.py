from allauth.account.forms import SignupForm
from django import forms
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3,label=False)
