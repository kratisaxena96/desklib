from django.contrib import admin
from documents.models import Document, File, Page


class FileInline(admin.TabularInline):
    model = File


class PageInline(admin.TabularInline):
    model = Page


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'key')
    # prepopulated_fields = {'slug': ('title',)}
    inlines = [
        FileInline,
        PageInline
    ]

    def get_form(self, request, obj=None, **kwargs):
        # Proper kwargs are form, fields, exclude, formfield_callback
        if obj:  # obj is not None, so this is a change page
            pass
        else:  # obj is None, so this is an add page
            kwargs['exclude'] = ('title', 'slug', 'subjects', 'key', 'created', 'updated', 'seo_title', 'seo_description', 'seo_keywords',)

        return super(DocumentAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Document, DocumentAdmin)
