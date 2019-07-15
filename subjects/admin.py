from django.contrib import admin

# Register your models here.
from subjects.models import Subject


class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['title','description']
    list_display = ('name','tag_list')
    search_fields = ['name','description']

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.keywords.all())

admin.site.register(Subject, SubjectAdmin)

