from django.contrib import admin
from documents.models import Document, File, Page, Report, Issue
from subjects.models import Subject
from django.db.models import F

def publish_documents(modeladmin, request, queryset):
    for doc in queryset:
        if doc.is_published == False:
            doc.is_published = True
            doc.save()
publish_documents.short_description = 'Publish Documents'

def un_publish_documents(modeladmin, request, queryset):
    for doc in queryset:
        if doc.is_published == True:
            doc.is_published = False
            doc.save()
un_publish_documents.short_description = 'Un-Publish Documents'

class SubjectListFilter(admin.SimpleListFilter):

    title = 'Subjects'
    parameter_name = 'sub'
    default_value = None

    def lookups(self, request, model_admin):
        list_of_subjects = []
        queryset = Subject.objects.all()
        for sub in queryset:
            list_of_subjects.append(
                (str(sub.id), sub.name)
            )
        return sorted(list_of_subjects, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subjects__id=int(self.value()))
        return queryset




class FileInline(admin.TabularInline):
    raw_id_fields = ('document',)
    # readonly_fields = ('author',)
    exclude = ['author']
    model = File



class PageInline(admin.TabularInline):
    raw_id_fields = ('document',)
    # readonly_fields = ('author',)
    exclude = ['author']
    model = Page

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'key')
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    raw_id_fields = ('author',)
    search_fields = ['title','content']
    list_display = ('title','published_date','is_published','page','words','get_subjects' )
    list_filter = (SubjectListFilter, )
    actions = [publish_documents, un_publish_documents]


    inlines = [
        FileInline,
        PageInline
    ]

    def get_subjects(self, obj):
        return "\n".join([sub.name for sub in obj.subjects.all()])

    def get_queryset(self, request):
        queryset = super(DocumentAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('pages').prefetch_related('document_file').prefetch_related('pages__author').prefetch_related('document_file__author')
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        # Proper kwargs are form, fields, exclude, formfield_callback
        if obj:  # obj is not None, so this is a change page
            pass
        else:  # obj is None, so this is an add page
            kwargs['exclude'] = ('title', 'slug', 'subjects', 'key', 'created', 'updated', 'seo_title', 'seo_description', 'seo_keywords',)

        return super(DocumentAdmin, self).get_form(request, obj, **kwargs)



class IssueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Document, DocumentAdmin)

admin.site.register(Issue, IssueAdmin)
admin.site.register(Report)
