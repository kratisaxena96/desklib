from django.contrib import admin

# Register your models here.
from subjects.models import Subject, SubjectContent
from django import forms


# class SubjectModelForm( forms.ModelForm ):
#     description = forms.CharField( widget=forms.Textarea )
#     class Meta:
#         model = Subject
#         fields = ['description']

class SubjectContentInlineAdmin(admin.TabularInline):
    model = SubjectContent
    prepopulated_fields = {'slug': ('title', )}


class SubjectContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}


class SubjectAdmin(admin.ModelAdmin):
    # form = SubjectModelForm
    search_fields = ['title', 'description']
    list_display = ('name', 'tag_list')
    search_fields = ['name', 'description']
    inlines = [SubjectContentInlineAdmin, ]

    def tag_list(self, obj):
        return u", ".join(list(obj.keywords.all().values_list('name',flat=True)))


admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectContent, SubjectContentAdmin )
