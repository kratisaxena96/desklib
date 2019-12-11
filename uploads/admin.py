from django.contrib import admin
from uploads.models import Upload
from subjects.models import Subject

# Register your models here.


# class SubjectListFilter(admin.SimpleListFilter):
#     title = 'Subjects'
#     parameter_name = 'sub'
#     default_value = None
#
#     def lookups(self, request, model_admin):
#         list_of_subjects = []
#         queryset = Subject.objects.all()
#         for sub in queryset:
#             list_of_subjects.append(
#                 (str(sub.id), sub.name)
#             )
#         return sorted(list_of_subjects, key=lambda tp: tp[1])
#
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(subjects__id=int(self.value()))
#         return queryset

class UplaodAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    raw_id_fields = ('author','subjects','author')
    search_fields = ['course_name', 'university']
    list_display = ('course_name', 'type', 'is_published', 'get_subjects')
    list_filter = ('subjects', 'type', 'is_published')

    def get_subjects(self, obj):
        return "\n".join([sub.name for sub in obj.subjects.all()])

admin.site.register(Upload, UplaodAdmin)