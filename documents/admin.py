from django.contrib import admin
from documents.models import Document, File, Page


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
    raw_id_fields = ('author',)

    inlines = [
        FileInline,
        PageInline
    ]

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

admin.site.register(Document, DocumentAdmin)
