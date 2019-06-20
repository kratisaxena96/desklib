from django.contrib import admin
from documents.models import Document



# Register your models here.

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'key')
    prepopulated_fields = {'slug': ('title',)}
    #
    # fieldsets = [('SEO', {
    #                 'fields': ('seo_title', 'seo_description', 'seo_keywords')
    #              })]

admin.site.register(Document, DocumentAdmin)