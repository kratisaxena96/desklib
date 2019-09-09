from allauth.account.forms import SignupForm, LoginForm, PasswordField
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _
from allauth.account import app_settings
from allauth.account.app_settings import AuthenticationMethod
from allauth.utils import get_username_max_length, set_form_field_order



class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    first_name = forms.CharField(max_length=40, label='First Name', widget=forms.TextInput(attrs={'placeholder':"First Name",'class':"form-control"}))
    last_name = forms.CharField(max_length=40, label='Last Name', widget=forms.TextInput(attrs={'placeholder':"Last Name",'class':"form-control"}))
    email = forms.EmailField(max_length=100, label='E-mail', widget=forms.EmailInput(attrs={'placeholder': "E-mail", 'class': "form-control"}))
    contact_no = PhoneNumberField(max_length=20, label='Contact No', widget=forms.TextInput(attrs={'placeholder':"e.g. +91-9876543210",'class':"form-control"}))
    password1 = forms.CharField(max_length=30, label='Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    password2 = forms.CharField(max_length=30, label='Confirm Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(label=_("Password"), widget=forms.PasswordInput(attrs={'class':"form-control"}))
        self.fields['password1'] = PasswordField(label=_("Password"), widget=forms.PasswordInput(attrs={'class':"form-control"}))
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields['password2'] = PasswordField(
                label=_("Password (again)"), widget=forms.PasswordInput(attrs={'class':"form-control"}))

        if hasattr(self, 'field_order'):
            set_form_field_order(self, self.field_order)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.contact_no = self.cleaned_data['contact_no']
        user.save()
        return user


class CustomLoginForm(LoginForm):
    password = forms.CharField(max_length=30, label='Password', widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class':"form-control placeholder"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)
        if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
            login_widget = forms.TextInput(attrs={'type': 'email',
                                                  'placeholder':
                                                  _('E-mail address'), 'class': "form-control",
                                                  'autofocus': 'autofocus'})
            login_field = forms.EmailField(label=_("E-mail"),
                                           widget=login_widget)
        elif app_settings.AUTHENTICATION_METHOD \
                == AuthenticationMethod.USERNAME:
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Username'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.CharField(
                label=_("Username"),
                widget=login_widget,
                max_length=get_username_max_length())
        else:
            assert app_settings.AUTHENTICATION_METHOD \
                == AuthenticationMethod.USERNAME_EMAIL
            login_widget = forms.TextInput(attrs={'placeholder':
                                                  _('Username or e-mail'),
                                                  'autofocus': 'autofocus'})
            login_field = forms.CharField(label=pgettext("field label",
                                                         "Login"),
                                          widget=login_widget)
        self.fields["login"] = login_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields['remember']

