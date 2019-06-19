from django.contrib import admin

# Register your models here.
from subjects.models import Subject


class SubjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Subject, SubjectAdmin)

