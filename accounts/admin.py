from django.contrib import admin
from accounts.models import UserAccount
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
# Register your models here.

class UserAccountForm(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all().prefetch_related('content_type'), widget=FilteredSelectMultiple("Option", is_stacked=False), required=False)

    class Meta:
        model = UserAccount
        exclude = []


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','full_name', 'email', 'contact_no', 'is_active')
    search_fields = ['email','username','first_name','last_name']
    actions = ['send_email']
    form = UserAccountForm

    ##function to send a promotional email to only 10 persons at a time.

    def send_email(modeladmin,request,queryset):
        from django.core.mail import send_mail,EmailMessage
        if queryset.count() <= 10:
            for item in queryset:
                if item.email:
                    sender=settings.DEFAULT_FROM_EMAIL
                    subject = 'welcome to GFG world'
                    message = f'Hi {item.username}, welcome to the Desklib'
                    email_from = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [item.email]
                    send_mail(subject, message, email_from, recipient_list)
                    messages.success(request,"done")
        else:
            messages.error(request, "you can only send email to  10 persons at a time.",fail_silently=True)

    send_email.short_description = "send email"

    def full_name(self, obj):
        return obj.get_full_name()


admin.site.register(UserAccount, UserAdmin)