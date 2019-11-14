from django.contrib import admin

# Register your models here.
from subjects.models import Subject
from django import forms


# class SubjectModelForm( forms.ModelForm ):
#     description = forms.CharField( widget=forms.Textarea )
#     class Meta:
#         model = Subject
#         fields = ['description']


class SubjectAdmin(admin.ModelAdmin):
    # form = SubjectModelForm
    search_fields = ['title','description']
    list_display = ('name','tag_list')
    search_fields = ['name','description']

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.keywords.all())

admin.site.register(Subject, SubjectAdmin)

