from django.contrib import admin
from accounts.models import UserAccount
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.admin.widgets import FilteredSelectMultiple

# Register your models here.

class UserAccountForm(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all().prefetch_related('content_type'), widget=FilteredSelectMultiple("Option", is_stacked=False), required=False)

    class Meta:
        model = UserAccount
        exclude = []


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'contact_no', 'is_active')
    search_fields = ['email']
    form = UserAccountForm

    def full_name(self, obj):
        return obj.get_full_name()


admin.site.register(UserAccount, UserAdmin)